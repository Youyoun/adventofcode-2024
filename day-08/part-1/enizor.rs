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

const fn antenna_pos(antenna: u8) -> usize {
    match antenna {
        b'0'..=b'9' => (antenna - b'0') as usize,
        b'a'..=b'z' => (10 + antenna - b'a') as usize,
        b'A'..=b'Z' => (36 + antenna - b'A') as usize,
        _ => 128,
    }
}

const fn build_antenna_pos_lut() -> [usize; 128] {
    let mut lut = [128; 128];
    let mut i = 0;
    while i < 128 {
        lut[i] = antenna_pos(i as u8);
        i += 1;
    }
    lut
}

const ANTENNA_POS_LUT: [usize; 128] = build_antenna_pos_lut();

struct AntennaLocations {
    count: [usize; 64],
    positions: Vec<usize>,
}

impl AntennaLocations {
    fn new() -> Self {
        Self {
            count: [0; 64],
            positions: vec![usize::MAX; 64 * 64],
        }
    }
    fn ensure_length(&mut self, count: usize) {
        if self.positions.len() < count * 64 {
            self.positions.resize(count * 64, usize::MAX);
        }
    }
    fn insert(&mut self, antenna: u8, cur: usize) {
        if antenna.is_ascii_alphanumeric() {
            let pos = ANTENNA_POS_LUT[antenna as usize];
            self.count[pos] += 1;
            self.ensure_length(self.count[pos]);
            self.positions[64 * (self.count[pos] - 1) + pos] = cur;
        }
    }
    fn list_frequencies(&self) -> impl Iterator<Item = usize> + '_ {
        self.count
            .iter()
            .enumerate()
            .filter_map(|(f, c)| if *c > 1 { Some(f) } else { None })
    }
    fn list_antennas(&self, pos: usize) -> Vec<usize> {
        self.positions
            .iter()
            .skip(pos)
            .step_by(64)
            .take(self.count[pos])
            .copied()
            .collect()
    }
}

fn run(input: &str) -> u32 {
    let grid = StrGrid::from_input(input);
    let bytes = input.as_bytes();
    let mut antinodes_set = VecBitSet::new(bitset_size(grid.height * grid.width));
    assert!(grid.height < usize::MAX / 2);
    assert!(grid.width < usize::MAX / 2);
    // locate all antennas
    let mut antennas = AntennaLocations::new();
    for (cur, b) in bytes.iter().enumerate() {
        antennas.insert(*b, cur);
    }
    for freq in antennas.list_frequencies() {
        // iterate over pairs of antennas
        let antennas_list = antennas.list_antennas(freq);
        for (i, a1) in antennas_list.iter().enumerate() {
            let antenna1 = grid.from_cur(*a1);
            for a2 in antennas_list.iter().skip(i + 1) {
                let antenna2 = grid.from_cur(*a2);
                // valid as long as overflowing does not get back into the map
                let dx = antenna1.x.wrapping_sub(antenna2.x);
                let dy = antenna1.y.wrapping_sub(antenna2.y);
                let p1 = Position {
                    x: antenna1.x.wrapping_add(dx),
                    y: antenna1.y.wrapping_add(dy),
                };
                if grid.valid_pos(p1) {
                    antinodes_set.set(grid.cur(p1));
                }
                let p2 = Position {
                    x: antenna2.x.wrapping_sub(dx),
                    y: antenna2.y.wrapping_sub(dy),
                };
                if grid.valid_pos(p2) {
                    antinodes_set.set(grid.cur(p2));
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
