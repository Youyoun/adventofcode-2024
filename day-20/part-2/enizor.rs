use std::env::args;
use std::time::Instant;

use aoc::enizor::{
    bitset::{bitset_size, VecBitSet},
    grid::{StrGrid, ALL_DIRECTIONS},
};

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"), THRESHOLD);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const THRESHOLD: usize = 100;
const MAX_CHEAT: usize = 20;

fn run(input: &str, threshold: usize) -> usize {
    let grid = StrGrid::from_input(input);
    let start = input.find('S').expect("failed to find starting point");
    let end = input.find('E').expect("failed to find ending point");
    let mut cur = start;
    let mut pos = grid.from_cur(cur);
    let mut visited = VecBitSet::new(bitset_size(input.len()));
    let mut path = Vec::with_capacity(input.len() / 2);
    path.push(pos);
    while cur != end {
        visited.set(cur);
        for d in ALL_DIRECTIONS {
            if let Some(new_pos) = grid.step(pos, d) {
                let new_cur: usize = grid.cur(new_pos);
                if (grid.data[new_cur] == b'.' || grid.data[new_cur] == b'E')
                    && !visited.test(new_cur)
                {
                    path.push(new_pos);
                    cur = new_cur;
                    pos = new_pos;
                    break;
                }
            }
        }
    }
    let mut res = 0;
    for (i, s) in path.iter().enumerate() {
        for (j, e) in path.iter().skip(i + threshold).enumerate() {
            let cost = s.x.abs_diff(e.x) + s.y.abs_diff(e.y);
            if cost <= MAX_CHEAT && j >= cost {
                res += 1;
            }
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
                50
            ),
            32 + 31 + 29 + 39 + 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
        );
    }
}

/*
There are 32 cheats that save 50 picoseconds.
There are 31 cheats that save 52 picoseconds.
There are 29 cheats that save 54 picoseconds.
There are 39 cheats that save 56 picoseconds.
There are 25 cheats that save 58 picoseconds.
There are 23 cheats that save 60 picoseconds.
There are 20 cheats that save 62 picoseconds.
There are 19 cheats that save 64 picoseconds.
There are 12 cheats that save 66 picoseconds.
There are 14 cheats that save 68 picoseconds.
There are 12 cheats that save 70 picoseconds.
There are 22 cheats that save 72 picoseconds.
There are 4 cheats that save 74 picoseconds.
There are 3 cheats that save 76 picoseconds.



There are 32 cheats that save 50 picoseconds.
There are 31 cheats that save 52 picoseconds.
There are 29 cheats that save 54 picoseconds.
There are 39 cheats that save 56 picoseconds.
There are 25 cheats that save 58 picoseconds.
There are 23 cheats that save 60 picoseconds.
There are 20 cheats that save 62 picoseconds.
There are 19 cheats that save 64 picoseconds.
There are 12 cheats that save 66 picoseconds.
There are 14 cheats that save 68 picoseconds.
There are 12 cheats that save 70 picoseconds.
There are 22 cheats that save 72 picoseconds.
There are 4 cheats that save 74 picoseconds.
There are 3 cheats that save 76 picoseconds.




*/
