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

fn run(input: &str) -> usize {
    // Your code goes here
    let mut left = Vec::with_capacity(input.len() / 16);
    let mut right = Vec::with_capacity(input.len() / 16);
    let mut even = true;
    let mut parser = Parser::from_input(&input);
    while let Some(v) = parser.parse_usize() {
        if even {
            left.push(v);
        } else {
            right.push(v);
        }
        even = !even;
        parser.skip_whitespace();
    }
    left.sort_unstable();
    right.sort_unstable();
    left.iter()
        .zip(right.iter())
        .map(|(l, r)| r.abs_diff(*l))
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("3   4
4   3
2   5
1   3
3   9
3   3"),
            11
        )
    }
}
