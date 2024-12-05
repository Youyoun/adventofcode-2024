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
    let mut r = 0;
    'outer: for line in input.split("\n") {
        let mut is = line.split_whitespace().map(|x| x.parse::<isize>().unwrap());
        let mut prev: isize = is.next().unwrap();
        let this = is.next().unwrap();
        let incr = this >= prev;
        let diff = this.abs_diff(prev);
        prev = this;
        if !(1..=3).contains(&diff) {
            continue 'outer;
        }
        for i in is {
            if incr && i <= prev || (!incr && i >= prev) {
                continue 'outer;
            }
            if i.abs_diff(prev) > 3 {
                continue 'outer;
            }
            prev = i;
        }
        r += 1;
    }
    r
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
            2
        )
    }
}
