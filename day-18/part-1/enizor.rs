use std::collections::VecDeque;
use std::env::args;
use std::time::Instant;

use aoc::enizor::bitset::ArrayBitSet;
use aoc::enizor::grid::{GridUtils, Position, ALL_DIRECTIONS};
use aoc::enizor::{bitset::bitset_size, parser::Parser};

fn main() {
    let now = Instant::now();
    let output = run::<LENGTH, BITSET_LENGTH, BYTES_NUMBER>(
        &args().nth(1).expect("Please provide an input"),
    );
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

// 0..=70
const LENGTH: usize = 71;
const BITSET_LENGTH: usize = bitset_size(LENGTH * LENGTH);
const BYTES_NUMBER: usize = 1024;

#[allow(dead_code)]
fn print<const L: usize, const N: usize>(grid: &ArrayBitSet<N>, visited: &ArrayBitSet<N>) {
    let mut s = String::from_utf8(vec![b'.'; L * (L + 1)]).unwrap();
    unsafe {
        for y in 0..L {
            for x in 0..L {
                let cur = L * y + x;
                let s_cur = (L + 1) * y + x;
                if grid.test(cur) {
                    assert!(!visited.test(cur));
                    s.as_bytes_mut()[s_cur] = b'#';
                } else if visited.test(cur) {
                    s.as_bytes_mut()[s_cur] = b'O';
                }
            }
            s.as_bytes_mut()[(L + 1) * y + L] = b'\n';
        }
    }
    eprintln!("{}", s);
}

fn shortest_path<const L: usize, const N: usize>(grid: &ArrayBitSet<N>) -> usize {
    let grid_utils = GridUtils {
        width: L,
        length: L,
    };
    let start: Position = Position { x: 0, y: 0 };
    let end: Position = Position { x: L - 1, y: L - 1 };
    let mut visited = ArrayBitSet::<N>::new();
    let mut queue = VecDeque::with_capacity(L * L);
    queue.push_back((0, start));
    while let Some((cost, pos)) = queue.pop_front() {
        if pos == end {
            return cost;
        }
        if cost > L * L {
            panic!("Failed somehow visited more than all the tiles!")
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
                    queue.push_back((new_cost, new_pos));
                }
            }
        }
    }
    usize::MAX
}

fn run<const L: usize, const N: usize, const S: usize>(input: &str) -> usize {
    let mut grid = ArrayBitSet::<N>::new();
    let mut parser = Parser::from_input(&input);
    let mut c = 0;
    while c < S && !parser.eof() {
        let x = parser.parse_usize().expect("failed to parse x coordinate");
        parser.cur += 1;
        let y = parser.parse_usize().expect("failed to parse y coordinate");
        parser.skip_whitespace();
        grid.set(L * y + x);
        c += 1;
    }
    shortest_path::<L, N>(&grid)
}

#[cfg(test)]
mod tests {
    use super::*;
    const EXEMPLE_LENGTH: usize = 7;
    const EXAMPLE_BITSET_SIZE: usize = bitset_size(LENGTH * LENGTH);
    const EXEMPLE_BYTES_NUMBER: usize = 12;

    #[test]
    fn run_test() {
        assert_eq!(
            run::<EXEMPLE_LENGTH, EXAMPLE_BITSET_SIZE, EXEMPLE_BYTES_NUMBER>(
                "5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"
            ),
            22
        )
    }
}
