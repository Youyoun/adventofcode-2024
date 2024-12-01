use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    // Your code goes here
    let mut left = Vec::with_capacity(input.len() / 16);
    let mut right = Vec::with_capacity(input.len() / 16);
    let mut even = true;
    for i in input.split_whitespace() {
        let v: usize = i.parse().expect("failed to parse input");
        if even {
            left.push(v);
        } else {
            right.push(v);
        }
        even = !even;
    }
    right.sort_unstable();
    left.iter()
        .map(|v| v * (right.partition_point(|x| *x < v + 1) - right.partition_point(|x| x < v)))
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("3   4
4   3
2   5
1   3
3   9
3   3"),
            31
        )
    }
}
