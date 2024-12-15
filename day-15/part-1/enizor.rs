use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

struct Warehouse {
    width: usize,
    height: usize,
    repr: String,
    pos_x: usize,
    pos_y: usize,
}

impl Warehouse {
    fn from_str(input: &str) -> Self {
        let mut width = 0;
        let mut height = 0;
        let mut pos_x = 0;
        let mut pos_y = 0;
        for line in input.lines() {
            if line.is_empty() {
                break;
            }
            if width == 0 {
                width = line.len() + 1;
            } else {
                assert_eq!(width, line.len() + 1);
            }
            if let Some((x, _)) = line
                .as_bytes()
                .iter()
                .enumerate()
                .find(|(_i, b)| **b == b'@')
            {
                pos_x = x;
                pos_y = height
            }
            height += 1;
        }
        let repr = input[..width * height].to_owned();
        Warehouse {
            width,
            height,
            repr,
            pos_x,
            pos_y,
        }
    }

    fn get(&self, x: usize, y: usize) -> u8 {
        self.repr.as_bytes()[y * self.width + x]
    }

    unsafe fn get_mut(&mut self, x: usize, y: usize) -> &mut u8 {
        &mut self.repr.as_bytes_mut()[y * self.width + x]
    }

    fn test_wall(&self, x: usize, y: usize) -> bool {
        self.get(x, y) == b'#'
    }

    fn test_box(&self, x: usize, y: usize) -> bool {
        self.get(x, y) == b'O'
    }

    fn swap(&mut self, x1: usize, y1: usize, x2: usize, y2: usize) {
        debug_assert_eq!(self.repr.as_bytes()[y2 * self.width + x2], b'.');
        // safety : we reuse existing bytes => still valid ASCII => still valid UTF-8
        unsafe {
            *self.get_mut(x2, y2) = self.get(x1, y1);
            *self.get_mut(x1, y1) = b'.';
        }
    }

    fn sum(&self) -> usize {
        let mut res = 0;
        for y in 0..self.height {
            for x in 0..self.width {
                if self.test_box(x, y) {
                    res += 100 * y + x;
                }
            }
        }
        res
    }

    fn move_dir(&mut self, dx: isize, dy: isize) {
        let x0 = self.pos_x as isize + dx;
        let y0 = self.pos_y as isize + dy;
        let mut x = x0;
        let mut y = y0;
        if !self.test_wall(x as usize, y as usize) {
            while self.test_box(x as usize, y as usize) {
                x += dx;
                y += dy;
            }
            if !self.test_wall(x as usize, y as usize) {
                if x0 != x || y0 != y {
                    self.swap(x0 as usize, y0 as usize, x as usize, y as usize);
                }
                self.swap(self.pos_x, self.pos_y, x0 as usize, y0 as usize);
                self.pos_x = x0 as usize;
                self.pos_y = y0 as usize;
            }
        }
    }
}

fn run(input: &str) -> usize {
    let mut warehouse = Warehouse::from_str(input);
    let lines = input.as_bytes()[warehouse.repr.len()..].split(|b| b == &b'\n');
    for line in lines {
        for b in line {
            match b {
                b'^' => warehouse.move_dir(0, -1),
                b'>' => warehouse.move_dir(1, 0),
                b'v' => warehouse.move_dir(0, 1),
                b'<' => warehouse.move_dir(-1, 0),
                _ => panic!("unexpected input!"),
            }
        }
    }
    warehouse.sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"),
            2028
        );
        assert_eq!(
            run("##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"),
            10092
        );
    }
}
