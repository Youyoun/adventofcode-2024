use aoc::enizor::bitset::*;
use aoc::enizor::grid::{
    Direction::{self, *},
    Position, StrGrid,
};
use std::env;
use std::env::args;
use std::thread;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

// return the next position before hitting a block, if exists
fn next_block(
    new_box: Position,
    pos: Position,
    dir: Direction,
    blocs_x: &[&[usize]],
    blocs_y: &[&[usize]],
) -> Option<Position> {
    match dir {
        Right => {
            let n = blocs_x[pos.y].partition_point(|&x| x <= pos.x);
            if n == blocs_x[pos.y].len() {
                if new_box.y == pos.y && new_box.x > pos.x {
                    Some(Position {
                        x: new_box.x - 1,
                        y: pos.y,
                    })
                } else {
                    None
                }
            } else if new_box.y == pos.y && new_box.x > pos.x {
                Some(Position {
                    x: (new_box.x.min(blocs_x[pos.y][n])) - 1,
                    y: pos.y,
                })
            } else {
                Some(Position {
                    x: blocs_x[pos.y][n] - 1,
                    y: pos.y,
                })
            }
        }
        Left => {
            let n = blocs_x[pos.y].partition_point(|&x| x <= pos.x);
            if n == 0 {
                if new_box.y == pos.y && new_box.x < pos.x {
                    Some(Position {
                        x: new_box.x + 1,
                        y: pos.y,
                    })
                } else {
                    None
                }
            } else if new_box.y == pos.y && new_box.x < pos.x {
                Some(Position {
                    x: new_box.x.max(blocs_x[pos.y][n - 1]) + 1,
                    y: pos.y,
                })
            } else {
                Some(Position {
                    x: blocs_x[pos.y][n - 1] + 1,
                    y: pos.y,
                })
            }
        }
        Down => {
            let n = blocs_y[pos.x].partition_point(|&y| y <= pos.y);
            if n == blocs_y[pos.x].len() {
                if new_box.x == pos.x && new_box.y > pos.y {
                    Some(Position {
                        y: new_box.y - 1,
                        x: pos.x,
                    })
                } else {
                    None
                }
            } else if new_box.x == pos.x && new_box.y > pos.y {
                Some(Position {
                    y: new_box.y.min(blocs_y[pos.x][n]) - 1,
                    x: pos.x,
                })
            } else {
                Some(Position {
                    y: blocs_y[pos.x][n] - 1,
                    x: pos.x,
                })
            }
        }
        Up => {
            let n = blocs_y[pos.x].partition_point(|&y| y <= pos.y);
            if n == 0 {
                if new_box.x == pos.x && new_box.y < pos.y {
                    Some(Position {
                        y: new_box.y + 1,
                        x: pos.x,
                    })
                } else {
                    None
                }
            } else if new_box.x == pos.x && new_box.y < pos.y {
                Some(Position {
                    y: new_box.y.max(blocs_y[pos.x][n - 1]) + 1,
                    x: pos.x,
                })
            } else {
                Some(Position {
                    y: blocs_y[pos.x][n - 1] + 1,
                    x: pos.x,
                })
            }
        }
    }
}

fn test_loop(
    grid: StrGrid<'_>,
    new_box: Position,
    mut pos: Position,
    mut dir: Direction,
    blocs_x: &[&[usize]],
    blocs_y: &[&[usize]],
) -> bool {
    let mut passages = VecBitSet::new(bitset_size(grid.grid_utils.width * grid.grid_utils.length));
    while let Some(pos2) = next_block(new_box, pos, dir, blocs_x, blocs_y) {
        if dir == Up {
            if passages.test(grid.cur(pos2)) {
                return true;
            } else {
                passages.set(grid.cur(pos2));
            }
        }
        dir.turn_indirect();
        pos = pos2;
    }
    false
}

fn run(input: &str) -> u32 {
    let grid = StrGrid::from_input(input);
    let cur = input
        .as_bytes()
        .iter()
        .position(|b| *b == b'^')
        .expect("failed to find starting position!");
    let start = grid.from_cur(cur);
    let mut blocs_x = vec![Vec::new(); grid.grid_utils.length];
    let mut blocs_y = vec![Vec::new(); grid.grid_utils.width];
    for (cur, _b) in input
        .as_bytes()
        .iter()
        .enumerate()
        .filter(|(_cur, b)| **b == b'#')
    {
        let pos = grid.from_cur(cur);
        blocs_x[pos.y].push(pos.x);
        blocs_y[pos.x].push(pos.y);
    }
    // use slices instead of Vecs to be able to share them when multithreading
    let blocs_x_refs = blocs_x.iter().map(|v| v.as_slice()).collect::<Vec<_>>();
    let blocs_y_refs = blocs_y.iter().map(|v| v.as_slice()).collect::<Vec<_>>();
    let mut res = 0;
    let nb_threads = env::var("ENIZOR_DAY_6_NB_THREADS")
        .ok()
        .and_then(|v| v.parse::<usize>().ok())
        .unwrap_or(0);
    if nb_threads < 2 {
        let mut dir = Up;
        let mut pos = start;
        let mut passsage = VecBitSet::new(bitset_size(input.len()));
        passsage.set(cur);
        while let Some(pos2) = grid.step(pos, dir) {
            if grid[pos2] == b'#' {
                dir.turn_indirect();
            } else {
                if !passsage.test(grid.cur(pos2))
                    && test_loop(grid, pos2, pos, dir, &blocs_x_refs, &blocs_y_refs)
                {
                    res += 1;
                }
                passsage.set(grid.cur(pos2));
                pos = pos2;
            }
        }
    } else {
        let b_x = blocs_x_refs.as_slice();
        let b_y = blocs_y_refs.as_slice();
        thread::scope(|s| {
            let mut handles = Vec::new();
            for i in 0..nb_threads - 1 {
                handles.push(s.spawn(move || {
                    let mut dir = Up;
                    let mut pos = start;
                    let mut count = 0;
                    let mut step = 0;
                    let mut passsage = VecBitSet::new(bitset_size(input.len()));
                    passsage.set(cur);
                    while let Some(pos2) = grid.step(pos, dir) {
                        if grid[pos2] == b'#' {
                            dir.turn_indirect();
                        } else {
                            if step % (nb_threads - 1) == i
                                && !passsage.test(grid.cur(pos2))
                                && test_loop(grid, pos2, pos, dir, b_x, b_y)
                            {
                                count += 1;
                            }
                            step += 1;
                            pos = pos2;
                            passsage.set(grid.cur(pos));
                        }
                    }
                    count
                }));
            }
            for h in handles {
                res += h.join().unwrap();
            }
        });
    }

    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."),
            6
        )
    }
}
