use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> isize {
    let mut res = 0;
    let mut i = 0;
    let bytes = input.as_bytes();
    let len = bytes.len();
    while let Some(p) = bytes[i..].iter().position(|&b| b == b'm') {
        i += p + 1;
        if i + 3 >= bytes.len() {
            continue;
        }
        if bytes[i] != b'u' || bytes[i + 1] != b'l' || bytes[i + 2] != b'(' {
            continue;
        }
        i += 3;
        let mut found = false;
        let mut lhs = 0;
        if i + 3 >= bytes.len() {
            continue;
        }
        for _ in 0..3 {
            if i == len || !bytes[i].is_ascii_digit() {
                break;
            } else {
                found = true;
                lhs *= 10;
                lhs += (bytes[i] - b'0') as isize;
                i += 1;
            }
        }
        if !found || i >= len || bytes[i] != b',' {
            continue;
        }
        i += 1;
        let mut rhs = 0;
        found = false;
        for _ in 0..3 {
            if i == len || !bytes[i].is_ascii_digit() {
                break;
            } else {
                found = true;
                rhs *= 10;
                rhs += (bytes[i] - b'0') as isize;
                i += 1;
            }
        }
        if found && i < len && bytes[i] == b')' {
            // dbg!(format!("mul({},{})",lhs, rhs));
            res += lhs * rhs;
            i += 1;
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
