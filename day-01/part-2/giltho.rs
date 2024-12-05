use std::collections::HashMap;
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
    let mut right: HashMap<isize, isize> = HashMap::with_capacity(1024);
    for line in input.split("\n") {
        let mut line = line.split("   ");
        let kl = line.next().unwrap().parse().unwrap();
        left.push(kl);
        let kr = line.next().unwrap().parse().unwrap();
        match right.get_mut(&kr) {
            Some(v) => {
                *v += 1;
            }
            None => {
                right.insert(kr, 1);
            }
        }
    }
    let mut r = 0;
    for k in left {
        r += k * right.get(&k).unwrap_or(&0);
    }
    r
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
            31
        )
    }
}
