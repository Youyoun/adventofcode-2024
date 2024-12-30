use std::collections::HashMap;
use std::env::args;
use std::time::Instant;

use aoc::enizor::bitset::{bitset_size, VecBitSet};
use aoc::enizor::parser::Parser;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}
/*
In particular, each buyer's secret number evolves into the next secret number in the sequence via the following process:

    Calculate the result of multiplying the secret number by 64. Then, mix this result into the secret number. Finally, prune the secret number.
    Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer. Then, mix this result into the secret number. Finally, prune the secret number.
    Calculate the result of multiplying the secret number by 2048. Then, mix this result into the secret number. Finally, prune the secret number.

Each step of the above process involves mixing and pruning:

    To mix a value into the secret number, calculate the bitwise XOR of the given value and the secret number. Then, the secret number becomes the result of that operation. (If the secret number is 42 and you were to mix 15 into the secret number, the secret number would become 37.)
    To prune the secret number, calculate the value of the secret number modulo 16777216. Then, the secret number becomes the result of that operation. (If the secret number is 100000000 and you were to prune the secret number, the secret number would become 16113920.)

*/

const ROUNDS: usize = 2000;
const MASK: usize = 16777216 - 1;

fn round(mut n: usize) -> usize {
    n ^= n << 6;
    n &= MASK;
    n ^= n >> 5;
    n &= MASK;
    n ^= n << 11;
    n &= MASK;
    n
}

// Price change is in -9..=9 => add 9 to have 0..=18
// can be represented using 5 bits
// a sequence of 4 price changes is in 4*5 bits

const SEQUENCE_MASK: usize = 0xFFFFF;

fn run(input: &str) -> usize {
    let mut p = Parser::from_input(&input);
    let mut g_observed_seqs = HashMap::new();
    while !p.eof() {
        let mut sequence = 0;
        let mut n = p.parse_usize().expect("failed to parse");
        let mut price = n % 10;
        p.skip_whitespace();
        let mut new_price;
        let mut new_chg;
        let mut seen = VecBitSet::new(bitset_size(1 << 20));
        for r in 0..ROUNDS {
            n = round(n);
            new_price = n % 10;
            new_chg = 9 + new_price - price;
            sequence <<= 5;
            sequence |= new_chg;
            sequence &= SEQUENCE_MASK;
            if r >= 4 && !seen.test(sequence) {
                seen.set(sequence);
                *g_observed_seqs.entry(sequence).or_insert(0) += new_price;
            }
            price = new_price;
        }
    }
    *g_observed_seqs.values().max().unwrap()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("1
2
3
2024
"),
            23
        )
    }
}
