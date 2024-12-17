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
        let p_x = 10000000000000 + parser.parse_usize()? as i64;
        debug_assert_eq!(parser.peek(), Some(&b','));
        parser.cur += 3;
        debug_assert_eq!(parser.peek(), Some(&b'='));
        parser.cur += 1;
        let p_y = 10000000000000 + parser.parse_usize()? as i64;
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
                if a >= 0 && b >= 0 {
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
