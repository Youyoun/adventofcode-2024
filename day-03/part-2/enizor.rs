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
    let mut dont = false;
    let mut parser = Parser::from_input(&input);
    while !parser.eof() {
        if dont {
            dont = !parser.find_str("do()");
            if dont {
                break;
            }
        } else {
            parser.find(|&&b| b == b'm' || b == b'd');
            if parser.eof() {
                break;
            }
            parser.cur -= 1;
            if parser.peek() == Some(&b'd') {
                parser.cur += 1;
                if parser.bytes[parser.cur..].starts_with(b"on't()") {
                    dont = true;
                    parser.cur += 6;
                }
            } else {
                parser.cur += 1;
                if parser.bytes[parser.cur..].starts_with(b"ul(") {
                    parser.cur += 3;
                    if let Some(mul) = parse_mul(&mut parser) {
                        res += mul;
                    }
                }
            }
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
            run("xxmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"),
            48
        );
    }
}
