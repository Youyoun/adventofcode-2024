use std::env::args;
use std::time::Instant;

use aoc::enizor::grid::*;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn trailhead_score(grid: &StrGrid<'_>, pos: Position) -> usize {
    let height = grid[pos];
    assert_eq!(height, b'0');
    let mut stack = vec![(pos, height)];
    let mut visited = vec![pos];
    let mut res = 0;
    while let Some((pos, height)) = stack.pop() {
        for d in ALL_DIRECTIONS {
            if let Some(pos2) = grid.step(pos, d) {
                if grid[pos2] == height + 1 && !visited.contains(&pos2) {
                    visited.push(pos2);
                    if height == b'8' {
                        res += 1;
                    } else {
                        stack.push((pos2, height + 1));
                    }
                }
            }
        }
    }
    res
}

fn run(input: &str) -> usize {
    let grid = StrGrid::from_input(input);
    let mut res = 0;
    for (cur, b) in input.as_bytes().iter().enumerate() {
        if *b == b'0' {
            res += trailhead_score(&grid, grid.from_cur(cur))
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
            run("...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9"),
            2
        );
        assert_eq!(
            run("..90..9
...1.98
...2..7
6543456
765.987
876....
987...."),
            4
        );
        assert_eq!(
            run("10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01"),
            1 + 2
        );
        assert_eq!(
            run("89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"),
            36
        )
    }
}
