use std::collections::HashMap;
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

fn parse(input: &[u8], map: &mut HashMap<usize, usize>) -> usize {
    let mut count = 0;
    let mut parser = Parser::from_input(&input);
    while let Some(v) = parser.parse_usize() {
        *map.entry(v).or_default() += 1;
        count += 1;
        parser.skip_whitespace();
    }
    count
}

fn split_digits(n: usize) -> Option<(usize, usize)> {
    let mut left = n;
    let mut right = 0;
    let mut right_ceil = 1;
    while left >= right_ceil {
        right += (left % 10) * right_ceil;
        right_ceil *= 10;
        left /= 10;
    }
    if left * 10 >= right_ceil {
        Some((left, right))
    } else {
        None
    }
}

fn run(input: &str) -> usize {
    let mut current_stones = HashMap::<usize, usize>::new();
    let mut next_stones = HashMap::<usize, usize>::new();
    let mut stone_count = parse(input.as_bytes(), &mut current_stones);
    for _ in 0..75 {
        for (&id, &count) in current_stones.iter() {
            if id == 0 {
                *next_stones.entry(1).or_default() += count;
            } else if let Some((l, r)) = split_digits(id) {
                *next_stones.entry(l).or_default() += count;
                *next_stones.entry(r).or_default() += count;
                stone_count += count;
            } else {
                *next_stones.entry(id * 2024).or_default() += count;
            }
        }
        std::mem::swap(&mut current_stones, &mut next_stones);
        next_stones.clear();
    }
    stone_count
}
