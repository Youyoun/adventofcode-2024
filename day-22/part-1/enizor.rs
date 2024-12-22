use std::env::args;
use std::time::Instant;

use aoc::enizor::parser::Parser;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const ROUNDS: usize = 2000;
const MASK: usize = 0xFFFFFF;

fn round(mut n: usize) -> usize {
    n ^= n << 6;
    n &= MASK;
    n ^= n >> 5;
    n &= MASK;
    n ^= n << 11;
    n &= MASK;
    n
}

fn run(input: &str) -> usize {
    let mut p = Parser::from_input(&input);
    let mut res = 0;
    while !p.eof() {
        let mut n = p.parse_usize().expect("failed to parse");
        p.skip_whitespace();
        for _r in 0..ROUNDS {
            n = round(n);
        }
        res += n;
    }
    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("1
10
100
2024
"),
            37327623
        )
    }
}
