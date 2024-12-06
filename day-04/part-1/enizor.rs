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

fn straight(grid: StrGrid<'_>, mut pos: Position, dir: Direction) -> Option<[u8; 3]> {
    let mut res = [0; 3];
    for r in res.iter_mut() {
        pos = grid.step(pos, dir)?;
        *r = grid[pos];
    }
    Some(res)
}

fn diagonal(
    grid: StrGrid<'_>,
    mut pos: Position,
    dir1: Direction,
    dir2: Direction,
) -> Option<[u8; 3]> {
    let mut res = [0; 3];
    for r in res.iter_mut() {
        pos = grid.step(pos, dir1)?;
        pos = grid.step(pos, dir2)?;
        *r = grid[pos];
    }
    Some(res)
}

const MAS: [u8; 3] = [b'M', b'A', b'S'];
const AMX: [u8; 3] = [b'A', b'M', b'X'];

fn run(input: &str) -> isize {
    let mut res = 0;
    let grid = StrGrid::from_input(input);
    for cur in 0..input.len() - 1 {
        let pos = grid.from_cur(cur);
        if grid[pos] == b'X' {
            if straight(grid, pos, Right) == Some(MAS) {
                res += 1;
            }
            if straight(grid, pos, Down) == Some(MAS) {
                res += 1;
            }
            if diagonal(grid, pos, Right, Down) == Some(MAS) {
                res += 1;
            }
            if diagonal(grid, pos, Right, Up) == Some(MAS) {
                res += 1;
            }
        } else if grid[pos] == b'S' {
            if straight(grid, pos, Right) == Some(AMX) {
                res += 1;
            }
            if straight(grid, pos, Down) == Some(AMX) {
                res += 1;
            }
            if diagonal(grid, pos, Right, Down) == Some(AMX) {
                res += 1;
            }
            if diagonal(grid, pos, Right, Up) == Some(AMX) {
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
            run("MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"),
            18
        )
    }
}
