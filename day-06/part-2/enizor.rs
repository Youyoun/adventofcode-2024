use aoc::enizor::bitset::*;
use aoc::enizor::grid::{
    Direction::{self, *},
    Position, StrGrid,
};
use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn test_loop(grid: StrGrid<'_>, new_box: Position, mut pos: Position, mut dir: Direction) -> bool {
    let mut passages = [
        VecBitSet::new(bitset_size(grid.width * grid.height)),
        VecBitSet::new(bitset_size(grid.width * grid.height)),
        VecBitSet::new(bitset_size(grid.width * grid.height)),
        VecBitSet::new(bitset_size(grid.width * grid.height)),
    ];
    while let Some(pos2) = grid.step(pos, dir) {
        if pos2 == new_box || grid[pos2] == b'#' {
            dir.turn_indirect();
        } else {
            if passages[dir as usize].test(grid.cur(pos2)) {
                return true;
            }
            pos = pos2;
            passages[dir as usize].set(grid.cur(pos));
        }
    }
    false
}

fn run(input: &str) -> u32 {
    let grid = StrGrid::from_input(input);
    let cur = input
        .as_bytes()
        .iter()
        .position(|b| *b == b'^')
        .expect("failed to find starting position!");
    let start = grid.from_cur(cur);
    let mut pos = start;
    let mut passsage = VecBitSet::new(bitset_size(grid.width * grid.height));
    passsage.set(cur);
    let mut dir = Up;
    let mut res = 0;
    while let Some(pos2) = grid.step(pos, dir) {
        if grid[pos2] == b'#' {
            dir.turn_indirect();
        } else {
            if !passsage.test(grid.cur(pos2)) && test_loop(grid, pos2, pos, dir) {
                res += 1;
            }
            pos = pos2;
            passsage.set(grid.cur(pos));
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
            6
        )
    }
}
