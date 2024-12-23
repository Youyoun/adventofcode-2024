use std::cmp::Reverse;
use std::time::Instant;
use std::{collections::BinaryHeap, env::args};

use aoc::enizor::bitset::{bitset_size, VecBitSet};
use aoc::enizor::grid::{Direction::*, StrGrid};

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const MOVE_COST: usize = 1;
const TURN_COST: usize = 1000;

fn run(input: &str) -> usize {
    let grid = StrGrid::from_input(input);
    let start_cur = input
        .as_bytes()
        .iter()
        .enumerate()
        .find(|(_i, b)| **b == b'S')
        .expect("failed to find start point!")
        .0;
    let mut visited = VecBitSet::new(bitset_size(input.len() * 4));
    let mut queue = BinaryHeap::new();
    queue.push(Reverse((0, grid.from_cur(start_cur), Right)));
    queue.push(Reverse((2 * TURN_COST, grid.from_cur(start_cur), Left)));
    while let Some(Reverse((cost, pos, mut dir))) = queue.pop() {
        dir.turn_indirect();
        for i in 0..3 {
            let new_cost = if i != 1 {
                cost + MOVE_COST + TURN_COST
            } else {
                cost + MOVE_COST
            };
            if let Some(new_pos) = grid.step(pos, dir) {
                let new_cur = grid.cur(new_pos);
                if !visited.test(new_cur * 4 + dir as usize) {
                    match grid.data[new_cur] {
                        b'#' | b'S' => {}
                        b'E' => return new_cost,
                        b'.' => {
                            queue.push(Reverse((new_cost, new_pos, dir)));
                        }
                        _ => panic!("unexpected input at {}", new_cur),
                    }
                }
            }
            dir.turn_direct();
        }
        visited.set(grid.cur(pos) * 4 + dir as usize);
    }

    0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"),
            7036
        );
        assert_eq!(
            run("#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"),
            11048
        );
    }
}
