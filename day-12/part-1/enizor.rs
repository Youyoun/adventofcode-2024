use std::env::args;
use std::time::Instant;

use aoc::enizor::bitset::{bitset_size, VecBitSet};
use aoc::enizor::grid::{StrGrid, ALL_DIRECTIONS};

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let mut price = 0;
    let grid = StrGrid::from_input(input);
    let mut visited = VecBitSet::new(bitset_size(input.len()));
    for cur in 0..input.len() {
        let pos = grid.from_cur(cur);
        if grid.valid_pos(pos) && !visited.test(cur) {
            let mut area = 0;
            let mut perimeter = 0;
            let mut stack = vec![pos];
            let plant = grid[pos];
            while let Some(pos) = stack.pop() {
                if visited.test(grid.cur(pos)) {
                    continue;
                }
                visited.set(grid.cur(pos));
                area += 1;
                perimeter += 4;
                for dir in ALL_DIRECTIONS {
                    if let Some(neighbor) = grid.step(pos, dir) {
                        if grid[neighbor] == plant {
                            perimeter -= 1;
                            stack.push(neighbor);
                        }
                    }
                }
            }
            price += area * perimeter;
        }
    }
    price
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("AAAA
BBCD
BBCC
EEEC"),
            140
        );
        assert_eq!(
            run("OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"),
            772
        );
        assert_eq!(
            run("RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"),
            1930
        );
    }
}
