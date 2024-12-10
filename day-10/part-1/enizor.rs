use std::env::args;
use std::time::Instant;
use std::usize;

use aoc::enizor::bitset::{bitset_size, ArrayBitSet};
use aoc::enizor::grid::*;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn trailhead_score(grid: &StrGrid<'_>, start: Position) -> usize {
    let height = grid[start];
    assert_eq!(height, b'0');
    let mut stack = Vec::new();
    stack.push((start, height));
    let mut res = 0;
    let mut visits = ArrayBitSet::<{ bitset_size(19 * 19) }>::new();
    while let Some((pos, height)) = stack.pop() {
        for dir in ALL_DIRECTIONS {
            if let Some(pos2) = grid.step(pos, dir) {
                if grid[pos2] == height + 1 {
                    let reduced_pos = 9 + start.x - pos2.x + 19 * (9 + start.y - pos2.y);
                    if !visits.test(reduced_pos) {
                        visits.set(reduced_pos);
                        if height == b'8' {
                            res += 1;
                        } else {
                            stack.push((pos2, height + 1));
                        }
                    }
                }
            }
        }
    }
    res
}

fn run(input: &str) -> usize {
    let grid = StrGrid::from_input(input);
    let mut scores = Vec::with_capacity(input.len());
    scores.resize_with(input.len(), || (0, 0));
    let mut res = 0;
    for (cur, b) in input.as_bytes().iter().enumerate() {
        if *b == b'0' {
            res += trailhead_score(&grid, grid.from_cur(cur));
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
            run("...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9"),
            2
        );
        assert_eq!(
            run("..90..9
...1.98
...2..7
6543456
765.987
876....
987...."),
            4
        );
        assert_eq!(
            run("10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01"),
            1 + 2
        );
        assert_eq!(
            run("89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"),
            36
        )
    }
}
