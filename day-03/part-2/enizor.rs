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
    let mut dont = false;
    while let Some(p) = bytes[i..].iter().position(|&b| b == b'm' || b == b'd') {
        i += p + 1;
        if i + 4 >= bytes.len() {
            continue;
        }
        if bytes[i - 1] == b'd' {
            if bytes[i] == b'o' {
                if bytes[i + 1] == b'(' && bytes[i + 2] == b')' {
                    i += 3;
                    dont = false;
                } else if i + 6 < len
                    && bytes[i + 1] == b'n'
                    && bytes[i + 2] == b'\''
                    && bytes[i + 3] == b't'
                    && bytes[i + 4] == b'('
                    && bytes[i + 5] == b')'
                {
                    i += 6;
                    dont = true;
                }
            }
            continue;
        }
        if dont || bytes[i] != b'u' || bytes[i + 1] != b'l' || bytes[i + 2] != b'(' {
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
            run("xxmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"),
            48
        );
    }
}
