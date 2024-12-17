use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn valid(line: &[isize]) -> bool {
    let mut line = line.into_iter().copied();
    let mut prev: isize = line.next().unwrap();
    let this = line.next().unwrap();
    let incr = this >= prev;
    let diff = this.abs_diff(prev);
    prev = this;
    if !(1..=3).contains(&diff) {
        return false;
    }
    for i in line {
        if incr && i <= prev || (!incr && i >= prev) {
            return false;
        }
        if i.abs_diff(prev) > 3 {
            return false;
        }
        prev = i;
    }
    true
}

fn valid_minus_one(line: &[isize]) -> bool {
    std::iter::once(line.to_vec())
        .chain((0..line.len()).map(|n| {
            line.iter()
                .enumerate()
                .filter_map(|(i, v)| if i == n { None } else { Some(*v) })
                .collect()
        }))
        .any(|vec: Vec<_>| valid(&vec))
}

fn run(input: &str) -> usize {
    input
        .split("\n")
        .map(|line| {
            let vec: Vec<_> = line
                .split_ascii_whitespace()
                .map(|x| x.parse::<isize>().unwrap())
                .collect();
            vec
        })
        .filter(|vec| valid_minus_one(vec))
        .count()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run(r"7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"),
            4
        )
    }
}
