use std::cmp::Reverse;
use std::fs::DirBuilder;
use std::time::Instant;
use std::usize;
use std::{collections::BinaryHeap, env::args};

use aoc::enizor::bitset::{bitset_size, VecBitSet};
use aoc::enizor::grid::{Direction::*, StrGrid, ALL_DIRECTIONS};
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
    let mut start_bitset = VecBitSet::new(bitset_size(input.len()));
    start_bitset.set(start_cur);
    // vector of cost to be there at that direction
    let mut costs_map = vec![[(usize::MAX, usize::MAX); 4]; input.len()];
    let mut bitsets = vec![start_bitset];
    let mut max_cost = usize::MAX;
    let mut good_positions = VecBitSet::new(bitset_size(input.len()));
    while let Some(Reverse((cost, pos, dir, bitset_id))) = queue.pop() {
        if cost >= max_cost {
            break;
        }
        let new_cost = cost + TURN_COST;
        let cur = grid.cur(pos);
        {
            let mut new_dir = dir;
            new_dir.turn_direct();
            let (map_cost, map_bitset_id) = &mut costs_map[cur][new_dir as usize];
            if *map_cost > new_cost {
                *map_cost = new_cost;
                let new_id = bitsets.len();
                bitsets.push(VecBitSet {
                    bits: bitsets[bitset_id].bits.clone(),
                });
                queue.push(Reverse((new_cost, pos, new_dir, new_id)));
                *map_bitset_id = new_id;
            } else if *map_cost == new_cost && *map_bitset_id != bitset_id {
                let (orig, current) = get_2_mut(&mut bitsets, *map_bitset_id, bitset_id);
                *orig |= current;
            }
        }
        {
            let mut new_dir = dir;
            new_dir.turn_indirect();
            let (map_cost, map_bitset_id) = &mut costs_map[cur][new_dir as usize];
            if *map_cost > new_cost {
                *map_cost = new_cost;
                let new_id = bitsets.len();
                bitsets.push(VecBitSet {
                    bits: bitsets[bitset_id].bits.clone(),
                });
                queue.push(Reverse((new_cost, pos, new_dir, new_id)));
                *map_bitset_id = new_id;
            } else if *map_cost == new_cost && *map_bitset_id != bitset_id {
                let (orig, current) = get_2_mut(&mut bitsets, *map_bitset_id, bitset_id);
                *orig |= current;
            }
        }
        {
            if let Some(new_pos) = grid.step(pos, dir) {
                let new_cur = grid.cur(new_pos);
                let new_cost = cost + MOVE_COST;
                let (map_cost, map_bitset_id) = &mut costs_map[new_cur][dir as usize];
                if *map_cost > new_cost {
                    *map_cost = new_cost;
                    *map_bitset_id = bitset_id;
                    match grid.data[new_cur] {
                        b'#' | b'S' => {}
                        b'E' => {
                            bitsets[bitset_id].set(new_cur);
                            max_cost = new_cost;
                            good_positions |= &bitsets[bitset_id];
                        }
                        b'.' => {
                            bitsets[bitset_id].set(new_cur);
                            queue.push(Reverse((new_cost, new_pos, dir, bitset_id)));
                        }
                        _ => panic!("unexpected input at {}", new_cur),
                    }
                } else if *map_cost == new_cost && *map_bitset_id != bitset_id {
                    let (orig, current) = get_2_mut(&mut bitsets, *map_bitset_id, bitset_id);
                    *orig |= current;
                }
            }
        }
    }
    good_positions.count_ones()
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
