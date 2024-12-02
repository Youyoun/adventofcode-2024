use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

#[derive(Default, Copy, Clone, Debug)]
struct LevelValidation {
    ascending: Option<bool>,
    prev: Option<u32>,
}

fn run(input: &str) -> usize {
    input
        .lines()
        .filter_map(|report| {
            report
                .split_ascii_whitespace()
                .map(|s| s.parse::<u32>().expect("failed to parse input!"))
                .try_fold(LevelValidation::default(), |state, lvl| {
                    match (state.ascending, state.prev) {
                        // init
                        (_, None) => Some(LevelValidation {
                            ascending: None,
                            prev: Some(lvl),
                        }),
                        // fail conditions
                        (_, Some(p)) if p.abs_diff(lvl) > 3 || p == lvl => None,
                        (Some(b), Some(p)) if b != (p < lvl) => None,
                        // detect monotony direction
                        (None, Some(p)) => Some(LevelValidation {
                            ascending: Some(p < lvl),
                            prev: Some(lvl),
                        }),
                        // "normal" case
                        _ => Some(LevelValidation {
                            prev: Some(lvl),
                            ..state
                        }),
                    }
                })
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
            2
        )
    }
}
