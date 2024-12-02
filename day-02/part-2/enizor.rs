use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

#[inline]
fn monotony_direction(array: &[u32]) -> Option<bool> {
    if array.len() < 4 {
        None
    } else {
        let a = array[0];
        let b = array[1];
        let c = array[2];
        let d = array[3];
        Some((a < b) as usize + (b < c) as usize + (c < d) as usize >= 2)
    }
}

#[inline]
fn compatible(a: u32, b: u32, ascending: Option<bool>) -> bool {
    a != b && a.abs_diff(b) < 4 && (ascending.is_none() || (a < b) == ascending.unwrap())
}

fn validate_record(record: &[u32]) -> Option<()> {
    if record.is_empty() {
        return None;
    } else if record.len() < 3 {
        return Some(());
    }
    let ascending = monotony_direction(record);
    let mut drop_start = 0;
    let mut drop_end = record.len();
    for i in 1..record.len() {
        if !compatible(record[i - 1], record[i], ascending) {
            // must remove either i or i-1
            drop_start = drop_start.max(i - 1);
            drop_end = drop_end.min(i + 1);
            if i >= 2 && !compatible(record[i - 2], record[i], ascending) {
                // cannot remove i-1 => must remove i
                drop_start = i;
            }
            if i + 1 < record.len() && !compatible(record[i - 1], record[i + 1], ascending) {
                // cannot remove i => must remove i-1
                drop_end = drop_end.min(i);
            }
            if drop_end <= drop_start {
                return None;
            }
        }
    }
    Some(())
}

fn run(input: &str) -> usize {
    input
        .lines()
        .filter_map(|level| {
            validate_record(
                &level
                    .split_ascii_whitespace()
                    .map(|s| s.parse::<u32>().expect("failed to parse input!"))
                    .collect::<Vec<_>>(),
            )
        })
        .count()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"),
            4
        )
    }
}
