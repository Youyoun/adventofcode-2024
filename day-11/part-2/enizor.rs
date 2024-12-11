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

fn parse(input: &[u8], map: &mut HashMap<usize, usize>) -> usize {
    let mut v = None;
    let mut count = 0;
    for b in input {
        match b {
            b' ' | b'\n' => {
                count += 1;
                *map.entry(v.expect("unexpected whitespace!")).or_default() += 1;
                v = None
            }
            _ => {
                assert!(b.is_ascii_digit());
                let v_ref = v.get_or_insert(0);
                *v_ref *= 10;
                *v_ref += (b - b'0') as usize;
            }
        }
    }
    if let Some(val) = v {
        count += 1;
        *map.entry(val).or_default() += 1;
    }
    count
}

fn split_digits(n: usize) -> Option<(usize, usize)> {
    let mut left = n;
    let mut right = 0;
    let mut right_ceil = 1;
    while left >= right_ceil {
        right += (left % 10) * right_ceil;
        right_ceil *= 10;
        left /= 10;
    }
    if left * 10 >= right_ceil {
        Some((left, right))
    } else {
        None
    }
}

fn run(input: &str) -> usize {
    let mut current_stones = HashMap::<usize, usize>::new();
    let mut next_stones = HashMap::<usize, usize>::new();
    let mut stone_count = parse(input.as_bytes(), &mut current_stones);
    for _ in 0..75 {
        for (&id, &count) in current_stones.iter() {
            if id == 0 {
                *next_stones.entry(1).or_default() += count;
            } else if let Some((l, r)) = split_digits(id) {
                *next_stones.entry(l).or_default() += count;
                *next_stones.entry(r).or_default() += count;
                stone_count += count;
            } else {
                *next_stones.entry(id * 2024).or_default() += count;
            }
        }
        std::mem::swap(&mut current_stones, &mut next_stones);
        next_stones.clear();
    }
    stone_count
}
