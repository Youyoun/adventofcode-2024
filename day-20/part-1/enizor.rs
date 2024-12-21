use std::env::args;
use std::time::Instant;

use aoc::enizor::grid::{StrGrid, ALL_DIRECTIONS};

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"), THRESHOLD);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const THRESHOLD: usize = 100;

fn run(input: &str, threshold: usize) -> usize {
    let grid = StrGrid::from_input(input);
    let mut distances = vec![usize::MAX; input.len()];
    let start = input.find('S').expect("failed to find starting point");
    let end = input.find('E').expect("failed to find ending point");
    let mut cur = start;
    let mut pos = grid.from_cur(cur);
    distances[start] = 0;
    let mut path = Vec::with_capacity(input.len() / 2);
    let mut cheats = Vec::with_capacity(input.len() / 2);
    path.push(start);
    let mut next_cur = usize::MAX;
    let mut next_pos = pos;
    while cur != end {
        debug_assert!(distances[cur] < usize::MAX);
        for d in ALL_DIRECTIONS {
            if let Some(new_pos) = grid.step(pos, d) {
                let new_cur: usize = grid.cur(new_pos);
                if (grid.data[new_cur] == b'.' || grid.data[new_cur] == b'E')
                    && distances[new_cur] == usize::MAX
                {
                    distances[new_cur] = distances[cur] + 1;
                    path.push(new_cur);
                    next_cur = new_cur;
                    next_pos = new_pos;
                } else {
                    for d2 in ALL_DIRECTIONS {
                        if let Some(cheat_pos) = grid.step(new_pos, d2) {
                            let cheat_cur = grid.cur(cheat_pos);
                            if (grid.data[cheat_cur] == b'.' || grid.data[cheat_cur] == b'E')
                                && distances[cheat_cur] == usize::MAX
                            {
                                cheats.push((cur, grid.cur(cheat_pos)));
                            }
                        }
                    }
                }
            }
        }
        cur = next_cur;
        pos = next_pos;
    }
    let mut res = 0;
    for (s, e) in cheats {
        if distances[e] - distances[s] - 2 >= threshold {
            res += 1;
        }
    }
    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run(
                "###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############",
                10
            ),
            10
        )
    }
}
