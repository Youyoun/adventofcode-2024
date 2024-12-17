use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn parse_int(n: &[u8]) -> isize {
    n.iter().fold(0, |acc, &d| acc * 10 + (d - b'0') as isize)
}

fn run(input: &str) -> isize {
    let re = regex::bytes::Regex::new(r"mul\((\d+),(\d+)\)|don't\(\)|do\(\)").unwrap();
    let mut enabled = true;
    re.captures_iter(input.as_bytes())
        .map(|c| match &c[0] {
            b"don't()" => {
                enabled = false;
                0
            }
            b"do()" => {
                enabled = true;
                0
            }
            _ => {
                if enabled {
                    parse_int(&c[1]) * parse_int(&c[2])
                } else {
                    0
                }
            }
        })
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"),
            48
        )
    }
}
