use aoc::enizor::bitset::*;
use aoc::enizor::grid::*;
use std::env::args;
use std::time::Instant;
fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

// valid as long as overflowing does not gets back into the map
fn antinodes(antenna1: Position, antenna2: Position) -> (Position, Position) {
    let dx = antenna1.x.wrapping_sub(antenna2.x);
    let dy = antenna1.y.wrapping_sub(antenna2.y);
    let p1 = Position {
        x: antenna1.x.wrapping_add(dx),
        y: antenna1.y.wrapping_add(dy),
    };
    let p2 = Position {
        x: antenna2.x.wrapping_sub(dx),
        y: antenna2.y.wrapping_sub(dy),
    };
    (p1, p2)
}

fn run(input: &str) -> u32 {
    let grid = StrGrid::from_input(input);
    let bytes = input.as_bytes();
    let mut antinodes_set = VecBitSet::new(bitset_size(grid.height * grid.width));
    assert!(grid.height < usize::MAX / 2);
    assert!(grid.width < usize::MAX / 2);
    for (cur, b) in bytes.iter().enumerate() {
        if b.is_ascii_alphanumeric() {
            for (cur2, _) in bytes
                .iter()
                .skip(cur + 1)
                .enumerate()
                .filter(|&(_, v)| v == b)
            {
                let (a1, a2) = antinodes(grid.from_cur(cur), grid.from_cur(cur + 1 + cur2));
                if grid.valid_pos(a1) {
                    antinodes_set.set(grid.cur(a1));
                }
                if grid.valid_pos(a2) {
                    antinodes_set.set(grid.cur(a2));
                }
            }
        }
    }
    antinodes_set.count_ones()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......A...
..........
.........."),
            4
        );
        assert_eq!(
            run("......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#."),
            14
        )
    }
}
