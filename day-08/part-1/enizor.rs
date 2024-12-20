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

const DEFAULT_VAL: Vec<usize> = vec![];

fn run(input: &str) -> u32 {
    let bytes = input.as_bytes();
    let grid = StrGrid::from_input(input);
    let width = grid.grid_utils.width - 1;
    let height = grid.grid_utils.length;
    // locate all antennas
    let mut antennas = [DEFAULT_VAL; 128];
    for (cur, b) in bytes
        .iter()
        .enumerate()
        .filter(|(_cur, b)| b.is_ascii_alphanumeric())
    {
        antennas[*b as usize].push(cur);
    }
    let mut antinodes_set = VecBitSet::new(bitset_size(height * width));
    for positions in &antennas {
        // iterate over pairs of antennas
        for (i, a1_cur) in positions.iter().enumerate() {
            let a1 = grid.from_cur(*a1_cur);
            for a2_cur in positions.iter().skip(i + 1) {
                let a2 = grid.from_cur(*a2_cur);
                let dx = a1.x.wrapping_sub(a2.x);
                let dy = a1.y.wrapping_sub(a2.y);
                let mut pos = a1;
                pos.x = a1.x.wrapping_add(dx);
                pos.y = a1.y.wrapping_add(dy);
                if pos.x < width && pos.y < height {
                    antinodes_set.set(pos.x * height + pos.y);
                }
                pos.x = a2.x.wrapping_sub(dx);
                pos.y = a2.y.wrapping_sub(dy);
                if pos.x < width && pos.y < height {
                    antinodes_set.set(pos.x * height + pos.y);
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
