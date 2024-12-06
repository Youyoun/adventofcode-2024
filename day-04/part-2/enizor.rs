use aoc::enizor::grid::{Direction::*, Position, StrGrid};
use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn perimeter(grid: StrGrid<'_>, mut pos: Position) -> Option<[u8; 4]> {
    let mut res = [0; 4];
    pos = grid.step(pos, Up)?;
    pos = grid.step(pos, Left)?;
    res[0] = grid[pos];
    pos = grid.step(pos, Right)?;
    pos = grid.step(pos, Right)?;
    res[2] = grid[pos];
    pos = grid.step(pos, Down)?;
    pos = grid.step(pos, Down)?;
    res[1] = grid[pos];
    pos = grid.step(pos, Left)?;
    pos = grid.step(pos, Left)?;
    res[3] = grid[pos];
    Some(res)
}

const MS: [u8; 2] = [b'M', b'S'];
const SM: [u8; 2] = [b'S', b'M'];

fn run(input: &str) -> isize {
    let mut res = 0;
    let grid = StrGrid::from_input(input);
    for cur in 0..input.len() - 1 {
        let pos = grid.from_cur(cur);
        if grid[pos] == b'A' {
            if let Some(array) = perimeter(grid, pos) {
                if (array[..2] == MS || array[..2] == SM) && (array[2..] == MS || array[2..] == SM)
                {
                    res += 1;
                }
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
            9
        )
    }
}
