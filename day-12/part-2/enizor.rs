use std::env::args;
use std::time::Instant;

use aoc::enizor::bitset::{bitset_size, VecBitSet};
use aoc::enizor::grid::{Direction::*, StrGrid, ALL_DIRECTIONS};

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
            let mut sides = 0;
            let mut stack = vec![(pos, cur)];
            let plant = grid[pos];
            let mut fences: [VecBitSet; 4] =
                core::array::from_fn(|_| VecBitSet::new(bitset_size(input.len())));
            while let Some((pos, cur)) = stack.pop() {
                if visited.test(grid.cur(pos)) {
                    continue;
                }
                visited.set(grid.cur(pos));
                area += 1;
                let mut neighbors = [None; 4];
                for dir in ALL_DIRECTIONS {
                    neighbors[dir as usize] =
                        grid.step(pos, dir).map(|p| (p, grid.cur(p), grid[p]));
                }
                for dir in ALL_DIRECTIONS {
                    if let Some((npos, ncur, _id)) =
                        neighbors[dir as usize].filter(|(_pos, _cur, id)| *id == plant)
                    {
                        stack.push((npos, ncur));
                    } else {
                        fences[dir as usize].set(cur);
                        let to_check = match dir {
                            Up | Down => [Left, Right],
                            Left | Right => [Up, Down],
                        };
                        let mut side_fences = 0;
                        for dir2 in to_check {
                            if neighbors[dir2 as usize]
                                .filter(|(_npos, _ncur, id)| *id == plant)
                                .map(|(_npos, ncur, _id)| fences[dir as usize].test(ncur))
                                .unwrap_or(false)
                            {
                                side_fences += 1;
                            }
                        }
                        match side_fences {
                            0 => sides += 1, // new fence not connecting to any already built
                            1 => sides += 0, // extending an existing side
                            2 => sides -= 1, // joining 2 preexisting sides together into a single one
                            _ => panic!("too many neighbors for joining fences!"),
                        }
                    }
                }
            }
            price += area * sides;
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
            80
        );
        assert_eq!(
            run("OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"),
            436
        );
        assert_eq!(
            run("AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"),
            368
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
            1206
        );
    }
}
