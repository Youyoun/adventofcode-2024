use std::cmp::Reverse;
use std::time::Instant;
use std::{collections::BinaryHeap, env::args};

use aoc::enizor::bitset::{bitset_size, VecBitSet};
use aoc::enizor::grid::{Direction::*, StrGrid};
use aoc::enizor::utils::get_2_mut;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const MOVE_COST: usize = 1;
const TURN_COST: usize = 1000;

#[allow(dead_code)]
fn debug_path(input: &str, bs: &VecBitSet) {
    let mut s = input.to_owned();
    unsafe {
        for (i, c) in s.as_bytes_mut().iter_mut().enumerate() {
            if bs.test(i) {
                *c = b'O';
            }
        }
    }
    eprintln!("{}", s);
}

fn run(input: &str) -> u32 {
    let grid = StrGrid::from_input(input);
    let start_cur = input
        .as_bytes()
        .iter()
        .enumerate()
        .find(|(_i, b)| **b == b'S')
        .expect("failed to find start point!")
        .0;
    let mut queue = BinaryHeap::new();
    queue.push(Reverse((0, grid.from_cur(start_cur), Right, 0)));
    queue.push(Reverse((2 * TURN_COST, grid.from_cur(start_cur), Left, 1)));
    let start_bitset = VecBitSet::new(bitset_size(input.len()));
    // vector of cost to be there at that direction
    let mut costs_map = vec![[(usize::MAX, usize::MAX); 4]; input.len()];
    let mut bitsets = vec![start_bitset.clone(), start_bitset];
    let mut max_cost = usize::MAX;
    let mut good_positions = VecBitSet::new(bitset_size(input.len()));
    while let Some(Reverse((cost, pos, mut dir, bitset_id))) = queue.pop() {
        if cost > max_cost {
            break;
        }
        let cur = grid.cur(pos);
        if grid.data[cur] == b'E' {
            max_cost = cost;
            good_positions |= &bitsets[bitset_id];
            continue;
        }
        bitsets[bitset_id].set(cur);
        dir.turn_indirect();
        let mut need_clone = false;
        for i in 0..3 {
            let new_cost = if i != 1 {
                cost + MOVE_COST + TURN_COST
            } else {
                cost + MOVE_COST
            };
            if let Some(new_pos) = grid.step(pos, dir) {
                let new_cur = grid.cur(new_pos);
                let (map_cost, map_bitset_id) = &mut costs_map[new_cur][dir as usize];
                if *map_cost > new_cost {
                    match grid.data[new_cur] {
                        b'#' | b'S' => {}
                        b'E' | b'.' => {
                            let new_id = if need_clone {
                                bitsets.push(bitsets[bitset_id].clone());
                                bitsets.len() - 1
                            } else {
                                bitset_id
                            };
                            *map_cost = new_cost;
                            *map_bitset_id = new_id;
                            need_clone = true;
                            queue.push(Reverse((new_cost, new_pos, dir, new_id)));
                        }
                        _ => panic!("unexpected input at {}", new_cur),
                    }
                } else if *map_cost == new_cost && *map_bitset_id != bitset_id {
                    let (orig, current) = get_2_mut(&mut bitsets, *map_bitset_id, bitset_id);
                    *orig |= current;
                }
            }
            dir.turn_direct();
        }
    }
    // we never actually set the bit for the end position, so add 1
    good_positions.count_ones() + 1
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
            45
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
            64
        );
    }
}
