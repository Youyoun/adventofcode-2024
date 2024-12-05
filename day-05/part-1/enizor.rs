use aoc::enizor::bitset;
use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

// assumes order is total and all comparisons are in rules
fn check_order<const N: usize>(rules: &bitset::ArrayBitSet<N>, updates: &[usize]) -> usize {
    let mut sorted = true;
    for i in 0..updates.len() - 1 {
        if !rules.test(updates[i] * 100 + updates[i + 1]) {
            sorted = false;
            break;
        }
    }
    if sorted {
        updates[updates.len() / 2]
    } else {
        0
    }
}

fn run(input: &str) -> usize {
    let mut rules = bitset::ArrayBitSet::<{ bitset::bitset_size(100 * 100) }>::new();
    let mut i = 0;
    let bytes = input.as_bytes();
    while i < input.len() {
        if bytes[i] == b'\n' {
            i += 1;
            break;
        }
        let mut rule = 0;
        for j in 0..5 {
            let b = bytes[i + j];
            if j == 2 {
                assert_eq!(
                    b,
                    b'|',
                    "Expecting each page to have a 2-digit number in rule {}",
                    &input[i..i + 6]
                );
            } else {
                assert!(
                    b.is_ascii_digit(),
                    "Failed to parse page number in rule {}",
                    &input[i..i + 6]
                );
                rule *= 10;
                rule += (b - b'0') as usize;
            }
        }
        assert_eq!(
            bytes[i + 5],
            b'\n',
            "Expecting each page to have a 2-digit number, got rule {}",
            &input[i..i + 5]
        );
        rules.set(rule);
        i += 6;
    }
    let mut update = Vec::with_capacity(32);
    update.push(0);
    let mut res = 0;
    while i < input.len() {
        let b = bytes[i];
        match b {
            b'\n' => {
                res += check_order(&rules, &update);
                update.clear();
                update.push(0)
            }
            b',' => update.push(0),
            b'0'..=b'9' => {
                let v = update.last_mut().unwrap();
                *v *= 10;
                *v += (b - b'0') as usize;
                assert!(*v < 100);
            }
            _ => panic!("Failed to  parse input {} at {} ", b as char, i),
        }
        i += 1;
    }
    // in case of missing EOF linebreak
    res += check_order(&rules, &update);
    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"),
            143
        )
    }
}
