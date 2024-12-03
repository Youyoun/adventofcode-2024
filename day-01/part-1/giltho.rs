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
    let mut left: Vec<isize> = Vec::with_capacity(1024);
    let mut right: Vec<isize> = Vec::with_capacity(1024);
    for line in input.split("\n") {
        let mut line = line.split("   ");
        left.push(line.next().unwrap().parse().unwrap());
        right.push(line.next().unwrap().parse().unwrap());
    }
    left.sort_unstable();
    right.sort_unstable();
    let mut res = 0;
    for (i, j) in left.iter().zip(right) {
        res += (j - i).abs();
    }
    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run(r"3   4
4   3
2   5
1   3
3   9
3   3"),
            11
        )
    }
}
