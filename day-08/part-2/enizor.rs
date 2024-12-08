use aoc::enizor::bitset::*;
use aoc::enizor::grid::*;
use std::env::args;
use std::path::Iter;
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
    let bytes = input.as_bytes();
    let mut antinodes_set = VecBitSet::new(bitset_size(grid.height * grid.width));
    assert!(grid.height < usize::MAX / 2);
    assert!(grid.width < usize::MAX / 2);
    for (cur, b) in bytes.iter().enumerate() {
        if b.is_ascii_alphanumeric() {
            // let vec = vec![cur];

            // let vec = bytes.iter().skip(cur+1).enumerate().filter_map(|(cur, v)| if v == b { Some(cur)} else { None } ).collect::<Vec<_>>();
            for (cur2, _) in bytes
                .iter()
                .skip(cur + 1)
                .enumerate()
                .filter(|&(_, v)| v == b)
            {
                let antenna1 = grid.from_cur(cur);
                let antenna2 = grid.from_cur(cur + 1 + cur2);
                let dx = antenna1.x.wrapping_sub(antenna2.x);
                let dy = antenna1.y.wrapping_sub(antenna2.y);
                let mut pos = antenna1;
                while grid.valid_pos(pos) {
                    antinodes_set.set(grid.cur(pos));
                    pos.x = pos.x.wrapping_add(dx);
                    pos.y = pos.y.wrapping_add(dy);
                }
                pos = antenna2;
                while grid.valid_pos(pos) {
                    antinodes_set.set(grid.cur(pos));
                    pos.x = pos.x.wrapping_sub(dx);
                    pos.y = pos.y.wrapping_sub(dy);
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
            run("T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
.........."),
            9
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
            34
        )
    }
}
