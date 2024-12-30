use std::env::args;
use std::time::Instant;

use aoc::enizor::{
    bitset::{bitset_size, ArrayBitSet},
    utils::get_2_mut,
};

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const LENGTH: usize = 5;
const HEIGHT: usize = 6;

fn parse_schematic(bytes: &[u8]) -> ([u8; 5], bool, usize) {
    let mut pins = [0; 5];
    let schema_type = bytes[0];
    let is_lock = schema_type == b'#';
    // skip first line
    let mut cur = LENGTH + 1;
    let mut height = 0;
    while cur + LENGTH - 1 < bytes.len() {
        if bytes[cur] == b'\n' {
            if !is_lock {
                for pin in pins.iter_mut() {
                    *pin = height - *pin; // maximum pin height accepted by the key
                }
            }
            debug_assert_eq!(HEIGHT as u8, height);
            return (pins, schema_type == b'#', cur + 1);
        }
        for i in 0..LENGTH {
            if bytes[cur + i] == b'#' {
                pins[i] += 1;
            }
        }
        height += 1;
        cur += LENGTH + 1;
    }
    debug_assert_eq!(HEIGHT as u8, height);
    if !is_lock {
        for pin in pins.iter_mut() {
            *pin = height - *pin; // maximum pin height accepted by the key
        }
    }
    (pins, is_lock, cur + 1)
}

const MAX_NB_LOCK: usize = 512;
const LOCKS_BITSET_SIZE: usize = bitset_size(MAX_NB_LOCK);

fn run(input: &str) -> u32 {
    let bytes = input.as_bytes();
    let mut cur = 0;
    let mut keys = vec![];
    // at pos (length*HEIGHT+1, height), all set lock IDs have pin at length <= height
    let mut locks_bitset = core::array::from_fn::<_, { LENGTH * (HEIGHT + 1) }, _>(|_i| {
        ArrayBitSet::<LOCKS_BITSET_SIZE>::new()
    });
    let mut lock_id: usize = 0;
    while cur + 4 < bytes.len() {
        let (pins, is_lock, adv) = parse_schematic(&bytes[cur..]);
        cur += adv;
        if is_lock {
            for (i, &p) in pins.iter().enumerate() {
                locks_bitset[i + (p as usize * LENGTH)].set(lock_id);
            }
            lock_id += 1;
        } else {
            keys.push(pins);
        }
    }
    // we have set pin at length == height, now propagate for pin at length < height
    for pin in 0..LENGTH {
        for h in 0..HEIGHT {
            let (l1, l2) = get_2_mut(&mut locks_bitset, pin + LENGTH * h, pin + LENGTH * (h + 1));
            *l2 |= l1;
        }
    }
    let mut res = 0;
    for k in keys {
        let mut fitting_locks = ArrayBitSet::<LOCKS_BITSET_SIZE>::ones();
        for p in 0..LENGTH {
            fitting_locks &= &locks_bitset[p + LENGTH * (k[p] as usize)];
        }
        res += fitting_locks.count_ones();
    }
    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"),
            3
        )
    }
}
