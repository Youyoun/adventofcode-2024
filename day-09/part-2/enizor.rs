use std::env::args;
use std::time::Instant;

use aoc::enizor::bitset::{bitset_size, VecBitSet};

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let bytes = input.as_bytes();
    let mut res = 0;
    let mut fwd_cur = 0;
    let mut i = 0;
    let mut end_cur = bytes.len() - 1;
    if end_cur % 2 == 1 {
        end_cur -= 1;
    }
    let mut moved_bs = VecBitSet::new(bitset_size(input.len() / 2));
    while fwd_cur < bytes.len() {
        if fwd_cur % 2 == 0 {
            let size = (bytes[fwd_cur] - b'0') as usize;
            if !moved_bs.test(fwd_cur / 2) {
                res += fwd_cur * size * (size - 1 + 2 * i) / 4;
            }
            i += size;
        } else {
            let mut empty_space = (bytes[fwd_cur] - b'0') as usize;
            let mut mov_cur = end_cur;
            while empty_space > 0 && mov_cur > fwd_cur {
                let mut size = 0;
                let mut all_moved = mov_cur == end_cur;
                while mov_cur > 1 && mov_cur > fwd_cur {
                    if !moved_bs.test(mov_cur / 2) {
                        let tmp_size = (bytes[mov_cur] - b'0') as usize;
                        if tmp_size <= empty_space {
                            size = tmp_size;
                            moved_bs.set(mov_cur / 2);
                            break;
                        } else {
                            all_moved = false;
                        }
                    }
                    mov_cur -= 2;
                }
                if size == 0 {
                    break;
                }
                res += mov_cur * size * (size - 1 + 2 * i) / 4;
                if all_moved {
                    end_cur = mov_cur;
                }
                mov_cur -= 2;
                i += size;
                empty_space -= size;
            }
            i += empty_space;
        }
        fwd_cur += 1;
    }
    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            "00992111777.44.333....5555.6666.....8888.."
                .bytes()
                .enumerate()
                .map(|(c, v)| if v == b'.' {
                    0
                } else {
                    c * ((v - b'0') as usize)
                })
                .sum::<usize>(),
            2858
        );
        assert_eq!(run("2333133121414131402"), 2858);
        // pas 7823589391077
    }
}
