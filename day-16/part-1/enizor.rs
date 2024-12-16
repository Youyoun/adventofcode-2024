use std::cmp::Reverse;
use std::time::Instant;
use std::{collections::BinaryHeap, env::args};

use aoc::enizor::grid::{Direction::*, StrGrid, ALL_DIRECTIONS};

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
    let mut visited = vec![false; input.len()];
    let mut queue = BinaryHeap::new();
    queue.push(Reverse((0, grid.from_cur(start_cur), Right)));
    while let Some(Reverse((cost, pos, dir))) = queue.pop() {
        for new_dir in ALL_DIRECTIONS {
            if new_dir == dir {
                if let Some(new_pos) = grid.step(pos, dir) {
                    let new_cur = grid.cur(new_pos);
                    let new_cost = cost + MOVE_COST;
                    match grid.data[new_cur] {
                        b'#' | b'S' => {}
                        b'E' => return new_cost,
                        b'.' => {
                            queue.push(Reverse((new_cost, new_pos, dir)));
                        }
                        _ => panic!("unexpected input at {}", new_cur),
                    }
                }
            } else if !visited[grid.cur(pos)] {
                if dir as usize % 2 != new_dir as usize % 2 {
                    let new_cost = cost + TURN_COST;
                    queue.push(Reverse((new_cost, pos, new_dir)));
                } else {
                    let new_cost = cost + TURN_COST + TURN_COST;
                    queue.push(Reverse((new_cost, pos, new_dir)));
                }
            }
        }
        visited[grid.cur(pos)] = true;
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
