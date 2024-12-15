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

fn parse_line(line: &[u8]) -> (usize, Vec<usize>) {
    let mut parser = Parser::from_input(&line);
    let v = parser.parse_usize().unwrap();
    debug_assert_eq!(parser.peek(), Some(&b':'));
    parser.cur += 2;
    let mut inputs = Vec::with_capacity(16);
    while let Some(w) = parser.parse_usize() {
        inputs.push(w);
        parser.cur += 1;
    }
    (v, inputs)
}

fn valid_line(line: (usize, &[usize])) -> bool {
    let goal = line.0;
    let stack = line.1;
    if let Some((last, rest)) = stack.split_last() {
        if rest.is_empty() {
            goal == *last
        } else {
            (goal % last == 0 && valid_line((goal / last, rest)))
                || (goal > *last && valid_line((goal - last, rest)))
        }
    } else {
        false
    }
}

fn run(input: &str) -> usize {
    input
        .as_bytes()
        .split(|b| *b == b'\n')
        .map(parse_line)
        .map(|(goal, stack)| if valid_line((goal, &stack)) { goal } else { 0 })
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert!(valid_line((190, &[10, 19])));
        assert_eq!(
            run("190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"),
            3749
        )
    }
}
