use std::env::args;
use std::time::Instant;

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
    fn from_input(bytes: &[u8]) -> (Self, usize) {
        let mut cur = 0;
        while bytes[cur] == b'\n' {
            cur += 1;
        }
        cur += 11;
        assert_eq!(bytes[cur], b'+');
        cur += 1;
        let mut a_x = 0;
        while bytes[cur].is_ascii_digit() {
            a_x *= 10;
            a_x += (bytes[cur] - b'0') as i64;
            cur += 1;
        }
        assert_eq!(bytes[cur], b',');
        cur += 3;
        assert_eq!(bytes[cur], b'+');
        cur += 1;
        let mut a_y = 0;
        while bytes[cur].is_ascii_digit() {
            a_y *= 10;
            a_y += (bytes[cur] - b'0') as i64;
            cur += 1;
        }
        assert_eq!(bytes[cur], b'\n');
        cur += 12;
        assert_eq!(bytes[cur], b'+');
        cur += 1;
        let mut b_x = 0;
        while bytes[cur].is_ascii_digit() {
            b_x *= 10;
            b_x += (bytes[cur] - b'0') as i64;
            cur += 1;
        }
        assert_eq!(bytes[cur], b',');
        cur += 3;
        assert_eq!(bytes[cur], b'+');
        cur += 1;
        let mut b_y = 0;
        while bytes[cur].is_ascii_digit() {
            b_y *= 10;
            b_y += (bytes[cur] - b'0') as i64;
            cur += 1;
        }
        assert_eq!(bytes[cur], b'\n');
        cur += 9;
        assert_eq!(bytes[cur], b'=');
        cur += 1;
        let mut p_x = 0;
        while bytes[cur].is_ascii_digit() {
            p_x *= 10;
            p_x += (bytes[cur] - b'0') as i64;
            cur += 1;
        }
        p_x += 10000000000000;
        assert_eq!(bytes[cur], b',');
        cur += 3;
        assert_eq!(bytes[cur], b'=');
        cur += 1;
        let mut p_y = 0;
        while cur < bytes.len() && bytes[cur].is_ascii_digit() {
            p_y *= 10;
            p_y += (bytes[cur] - b'0') as i64;
            cur += 1;
        }
        p_y += 10000000000000;
        (
            ClawMachine {
                a_x,
                a_y,
                b_x,
                b_y,
                p_x,
                p_y,
            },
            cur,
        )
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
    let bytes = input.as_bytes();
    let mut cur = 0;
    let mut res = 0;
    while cur + 10 < bytes.len() {
        let (claw, c) = ClawMachine::from_input(&bytes[cur..]);
        cur += c;
        res += claw.token_cost()
    }
    res
}
