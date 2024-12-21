use std::cmp::Reverse;
use std::time::Instant;
use std::{collections::BinaryHeap, env::args};

use aoc::enizor::bitset::ArrayBitSet;
use aoc::enizor::grid::{GridUtils, Position, ALL_DIRECTIONS};
use aoc::enizor::{bitset::bitset_size, parser::Parser};

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

// 0..=70
const LENGTH: usize = 71;
// const LENGTH: usize = 7;

const BYTES_NUMBER: usize = 1024;
// const BYTES_NUMBER: usize = 12;

const START: Position = Position { x: 0, y: 0 };
const END: Position = Position {
    x: LENGTH - 1,
    y: LENGTH - 1,
};

#[allow(dead_code)]
fn print<const N: usize>(grid: &ArrayBitSet<N>, visited: &ArrayBitSet<N>) {
    let mut s = String::from_utf8(vec![b'.'; LENGTH * (LENGTH + 1)]).unwrap();
    unsafe {
        for y in 0..LENGTH {
            for x in 0..LENGTH {
                let cur = LENGTH * y + x;
                let s_cur = (LENGTH + 1) * y + x;
                if grid.test(cur) {
                    assert!(!visited.test(cur));
                    s.as_bytes_mut()[s_cur] = b'#';
                } else if visited.test(cur) {
                    s.as_bytes_mut()[s_cur] = b'O';
                }
            }
            s.as_bytes_mut()[(LENGTH + 1) * y + LENGTH] = b'\n';
        }
    }
    eprintln!("{}", s);
}

fn shortest_path<const N: usize>(grid: &ArrayBitSet<N>) -> usize {
    let grid_utils = GridUtils {
        width: LENGTH,
        length: LENGTH,
    };
    let mut visited = ArrayBitSet::<N>::new();
    let mut queue = BinaryHeap::new();
    queue.push(Reverse((0, START)));
    while let Some(Reverse((cost, pos))) = queue.pop() {
        if pos == END {
            return cost;
        }
        if cost > LENGTH * LENGTH {
            return usize::MAX;
        }
        if visited.test(grid_utils.cur(pos)) {
            continue;
        } else {
            visited.set(grid_utils.cur(pos));
        }
        for dir in ALL_DIRECTIONS {
            let new_cost = cost + 1;
            if let Some(new_pos) = grid_utils.step(pos, dir) {
                let new_cur = grid_utils.cur(new_pos);
                if !visited.test(new_cur) && !grid.test(new_cur) {
                    queue.push(Reverse((new_cost, new_pos)));
                }
            }
        }
    }
    usize::MAX
}

fn run(input: &str) -> String {
    let mut grid = ArrayBitSet::<{ bitset_size(LENGTH * LENGTH) }>::new();
    let mut parser = Parser::from_input(&input);
    // dichotomy between 0 and input.len()
    let mut points = Vec::with_capacity(input.len() / 6);
    while !parser.eof() {
        let x = parser.parse_usize().expect("failed to parse x coordinate");
        parser.cur += 1;
        let y = parser.parse_usize().expect("failed to parse y coordinate");
        parser.skip_whitespace();
        points.push((x, y));
    }
    let mut a = BYTES_NUMBER;
    let mut b = points.len() - 1;
    while a < b {
        let mid = (a + b) / 2;
        grid.clear();
        for (x, y) in &points[0..=mid] {
            grid.set(LENGTH * y + x);
        }
        if shortest_path(&grid) == usize::MAX {
            b = mid;
        } else {
            a = mid + 1;
        }
    }
    format!("{},{}", points[a].0, points[a].1)
}

#[cfg(test)]
mod tests {
    //     use super::*;

    //     #[test]
    //     fn run_test() {
    //         assert_eq!(
    //             run("5,4
    // 4,2
    // 4,5
    // 3,0
    // 2,1
    // 6,3
    // 2,4
    // 1,5
    // 0,6
    // 3,3
    // 2,6
    // 5,1
    // 1,2
    // 5,5
    // 2,5
    // 6,5
    // 1,4
    // 0,4
    // 6,4
    // 1,1
    // 6,1
    // 1,0
    // 0,5
    // 1,6
    // 2,0"),
    //             "6,1"
    //         )
    //     }
}
