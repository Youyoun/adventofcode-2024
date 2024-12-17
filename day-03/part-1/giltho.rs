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
    let re = regex::bytes::Regex::new(r"mul\((\d+),(\d+)\)").unwrap();
    re.captures_iter(input.as_bytes())
        .map(|c| {
            let (_, [lhs, rhs]) = c.extract();
            parse_int(lhs) * parse_int(rhs)
        })
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"),
            161
        )
    }
}
