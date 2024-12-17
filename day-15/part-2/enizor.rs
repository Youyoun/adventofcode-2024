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
    fn from_str(lines: &str) -> Self {
        let mut width = 0;
        let mut height = 0;
        let mut pos_x = 0;
        let mut pos_y = 0;
        let mut repr = String::with_capacity(lines.len());
        for line in lines.lines() {
            if line.is_empty() {
                break;
            }
            if width == 0 {
                width = 2 * line.len() + 1;
            } else {
                assert_eq!(width, 2 * line.len() + 1);
            }
            for (x, b) in line.as_bytes().iter().enumerate() {
                match b {
                    b'@' => {
                        repr.push_str("@.");
                        pos_x = 2 * x;
                        pos_y = height
                    }
                    b'#' => repr.push_str("##"),
                    b'O' => repr.push_str("[]"),
                    _ => repr.push_str(".."),
                };
            }
            repr.push('\n');
            height += 1;
        }
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

    fn swap(&mut self, x1: usize, y1: usize, x2: usize, y2: usize) {
        debug_assert_eq!(self.get(x2, y2), b'.');
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
                if self.get(x, y) == b'[' {
                    res += 100 * y + x;
                }
            }
        }
        res
    }

    fn can_move_dir(&mut self, x0: isize, y0: isize, dx: isize, dy: isize) -> bool {
        let x1 = x0 + dx;
        let y1 = y0 + dy;
        match (self.get(x1 as usize, y1 as usize), dx) {
            (b'.', _) => true,
            (b'#', _) => false,
            (b'[', 0) => self.can_move_dir(x1, y1, dx, dy) && self.can_move_dir(x1 + 1, y1, dx, dy),
            (b'[', 1) => self.can_move_dir(x1 + 1, y1, dx, dy),
            (b'[', -1) => self.can_move_dir(x1, y1, dx, dy),
            (b']', 0) => self.can_move_dir(x1 - 1, y1, dx, dy) && self.can_move_dir(x1, y1, dx, dy),
            (b']', 1) => self.can_move_dir(x1, y1, dx, dy),
            (b']', -1) => self.can_move_dir(x1 - 1, y1, dx, dy),
            _ => panic!("unexpected state!"),
        }
    }

    fn do_move_dir(&mut self, x0: isize, y0: isize, dx: isize, dy: isize) {
        let x1 = x0 + dx;
        let y1 = y0 + dy;
        match (self.get(x1 as usize, y1 as usize), dx) {
            (b'.', _) => {}
            (b'#', _) => panic!("faceplant!"),
            (b'[', 0) => {
                debug_assert_eq!(self.get(x1 as usize + 1, y1 as usize), b']');
                self.do_move_dir(x1, y1, dx, dy);
                self.do_move_dir(x1 + 1, y1, dx, dy);
            }
            (b'[', 1) => {
                debug_assert_eq!(self.get(x1 as usize + 1, y1 as usize), b']');
                self.do_move_dir(x1 + 1, y1, dx, dy);
                debug_assert_eq!(self.get(x1 as usize + 1, y1 as usize), b'.');
                self.swap(x1 as usize, y1 as usize, x1 as usize + 1, y1 as usize);
            }
            (b'[', -1) => {
                debug_assert_eq!(self.get(x1 as usize + 1, y1 as usize), b']');
                self.do_move_dir(x1, y1, dx, dy);
                debug_assert_eq!(self.get(x1 as usize, y1 as usize), b'.');
                self.swap(x1 as usize + 1, y1 as usize, x1 as usize, y1 as usize);
            }
            (b']', 0) => {
                debug_assert_eq!(self.get(x1 as usize - 1, y1 as usize), b'[');
                self.do_move_dir(x1, y1, dx, dy);
                self.do_move_dir(x1 - 1, y1, dx, dy);
            }
            (b']', 1) => {
                debug_assert_eq!(self.get(x1 as usize - 1, y1 as usize), b'[');
                self.do_move_dir(x1, y1, dx, dy);
                debug_assert_eq!(self.get(x1 as usize, y1 as usize), b'.');
                self.swap(x1 as usize - 1, y1 as usize, x1 as usize, y1 as usize);
            }
            (b']', -1) => {
                debug_assert_eq!(self.get(x1 as usize - 1, y1 as usize), b'[');
                self.do_move_dir(x1 - 1, y1, dx, dy);
                debug_assert_eq!(self.get(x1 as usize - 1, y1 as usize), b'.');
                self.swap(x1 as usize, y1 as usize, x1 as usize - 1, y1 as usize);
            }
            _ => panic!("unexpected state!"),
        }
        self.swap(x0 as usize, y0 as usize, x1 as usize, y1 as usize);
    }

    fn move_dir(&mut self, dx: isize, dy: isize) {
        if self.can_move_dir(self.pos_x as isize, self.pos_y as isize, dx, dy) {
            self.do_move_dir(self.pos_x as isize, self.pos_y as isize, dx, dy);
            self.pos_x = (self.pos_x as isize + dx) as usize;
            self.pos_y = (self.pos_y as isize + dy) as usize;
        }
    }
}

fn run(input: &str) -> usize {
    let mut warehouse = Warehouse::from_str(input);
    let warehouse_str_len = warehouse.height * (1 + ((warehouse.width - 1) / 2));
    let lines = input.as_bytes()[warehouse_str_len..].split(|b| b == &b'\n');
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
            run("#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"),
            618
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
            9021
        );
    }
}
