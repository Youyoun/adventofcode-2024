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

fn parse_mul(parser: &mut Parser) -> Option<usize> {
    let lhs = parser.parse_sized_nb(3)?;
    let _ = parser.next().filter(|&&b| b == b',')?;
    let rhs = parser.parse_sized_nb(3)?;
    let _ = parser.next().filter(|&&b| b == b')')?;
    Some(lhs * rhs)
}

fn run(input: &str) -> usize {
    let mut res = 0;
    let mut parser = Parser::from_input(&input);
    while parser.find_str("mul(") {
        if let Some(mul) = parse_mul(&mut parser) {
            res += mul;
        }
    }
    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"),
            161
        );
    }
}
