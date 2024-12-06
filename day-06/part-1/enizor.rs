use aoc::enizor::bitset::*;
use aoc::enizor::grid::{Direction::*, StrGrid};
use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> u32 {
    let grid = StrGrid::from_input(input);
    let mut passsage = VecBitSet::new(bitset_size(grid.width * grid.height));
    let cur = input
        .as_bytes()
        .iter()
        .position(|b| *b == b'^')
        .expect("failed to find starting position!");
    let mut pos = grid.from_cur(cur);
    passsage.set(cur);
    let mut dir = Up;
    while let Some(pos2) = grid.step(pos, dir) {
        if grid[pos2] == b'#' {
            dir.turn_indirect();
        } else {
            pos = pos2;
            passsage.set(grid.cur(pos));
        }
    }
    passsage.count_ones()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."),
            41
        )
    }
}
