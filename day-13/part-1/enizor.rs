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

#[derive(Debug, Clone, Copy, Default)]
struct ClawMachine {
    a_x: i64,
    a_y: i64,
    b_x: i64,
    b_y: i64,
    p_x: i64,
    p_y: i64,
}

impl ClawMachine {
    fn from_input(parser: &mut Parser) -> Option<Self> {
        parser.skip_whitespace();
        if parser.eof() {
            return None;
        }
        parser.cur += 11;
        debug_assert_eq!(parser.peek(), Some(&b'+'));
        parser.cur += 1;
        let a_x = parser.parse_usize()? as i64;
        debug_assert_eq!(parser.peek(), Some(&b','));
        parser.cur += 3;
        debug_assert_eq!(parser.peek(), Some(&b'+'));
        parser.cur += 1;
        let a_y = parser.parse_usize()? as i64;
        debug_assert_eq!(parser.peek(), Some(&b'\n'));
        parser.cur += 12;
        debug_assert_eq!(parser.peek(), Some(&b'+'));
        parser.cur += 1;
        let b_x = parser.parse_usize()? as i64;
        debug_assert_eq!(parser.peek(), Some(&b','));
        parser.cur += 3;
        debug_assert_eq!(parser.peek(), Some(&b'+'));
        parser.cur += 1;
        let b_y = parser.parse_usize()? as i64;
        debug_assert_eq!(parser.peek(), Some(&b'\n'));
        parser.cur += 9;
        debug_assert_eq!(parser.peek(), Some(&b'='));
        parser.cur += 1;
        let p_x = parser.parse_usize()? as i64;
        debug_assert_eq!(parser.peek(), Some(&b','));
        parser.cur += 3;
        debug_assert_eq!(parser.peek(), Some(&b'='));
        parser.cur += 1;
        let p_y = parser.parse_usize()? as i64;
        Some(ClawMachine {
            a_x,
            a_y,
            b_x,
            b_y,
            p_x,
            p_y,
        })
    }

    fn token_cost(&self) -> i64 {
        let det = self.a_x * self.b_y - self.a_y * self.b_x;
        if det == 0 {
            // button A & B are multiples of each other.
            if self.a_x * self.p_y - self.a_y * self.p_x == 0 {
                // infinite real solutions
                let m_x = self.a_x.min(self.b_x);
                let m_y = self.a_y.min(self.b_y);
                // check for lowest cost for integers
                if self.p_x % m_x == 0 && self.p_y % m_y == 0 {
                    // possible over integers
                    let use_b = self.a_x / self.b_x <= 3;
                    if use_b {
                        return (self.p_x / self.b_x) + (3 * ((self.p_x % self.b_x) / self.a_x));
                    } else {
                        return 3 * (self.p_x / self.a_x) + ((self.p_x % self.a_x) / self.b_x);
                    }
                }
            }
        } else {
            // only one (real) solution, check if it is an integer in [0,100]
            let mut a = self.b_y * self.p_x - self.b_x * self.p_y;
            let mut b = self.a_x * self.p_y - self.a_y * self.p_x;
            if a % det == 0 && b % det == 0 {
                a /= det;
                b /= det;
                if (0..=100).contains(&a) && (0..=100).contains(&b) {
                    return 3 * a + b;
                }
            }
        }
        0
    }
}

fn run(input: &str) -> i64 {
    let mut parser = Parser::from_input(&input);
    let mut res = 0;
    while let Some(claw) = ClawMachine::from_input(&mut parser) {
        res += claw.token_cost()
    }
    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            ClawMachine {
                a_x: 94,
                a_y: 34,
                b_x: 22,
                b_y: 67,
                p_x: 8400,
                p_y: 5400,
            }
            .token_cost(),
            280
        );
        assert_eq!(
            ClawMachine {
                a_x: 26,
                a_y: 66,
                b_x: 67,
                b_y: 21,
                p_x: 12748,
                p_y: 12176,
            }
            .token_cost(),
            0
        );
        assert_eq!(
            ClawMachine {
                a_x: 17,
                a_y: 86,
                b_x: 84,
                b_y: 37,
                p_x: 7870,
                p_y: 6450,
            }
            .token_cost(),
            200
        );
        assert_eq!(
            ClawMachine {
                a_x: 69,
                a_y: 23,
                b_x: 27,
                b_y: 71,
                p_x: 18641,
                p_y: 10279,
            }
            .token_cost(),
            0
        );
        assert_eq!(
            ClawMachine {
                a_x: 1,
                a_y: 1,
                b_x: 2,
                b_y: 2,
                p_x: 9,
                p_y: 9,
            }
            .token_cost(),
            7
        );
        assert_eq!(
            ClawMachine {
                a_x: 2,
                a_y: 2,
                b_x: 1,
                b_y: 1,
                p_x: 9,
                p_y: 9,
            }
            .token_cost(),
            9
        );
        assert_eq!(
            ClawMachine {
                a_x: 8,
                a_y: 8,
                b_x: 2,
                b_y: 2,
                p_x: 9,
                p_y: 9,
            }
            .token_cost(),
            0
        );
        assert_eq!(
            ClawMachine {
                a_x: 8,
                a_y: 8,
                b_x: 2,
                b_y: 2,
                p_x: 22,
                p_y: 22,
            }
            .token_cost(),
            9
        );
        assert_eq!(
            run("Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"),
            480
        )
    }
}
