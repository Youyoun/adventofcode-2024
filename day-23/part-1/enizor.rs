use std::env::args;
use std::time::Instant;

use aoc::enizor::bitset::{bitset_size, ArrayBitSet};

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const MAX_ID: usize = 32 * 32;
const MAX_PAIR: usize = MAX_ID * MAX_ID;

const MASK: usize = (1 << 5) - 1;

fn computer_to_id(computer: &[u8]) -> usize {
    debug_assert_eq!(
        computer.len(),
        2,
        "errror parsing {}",
        core::str::from_utf8(computer).unwrap()
    );
    ((computer[1] - b'a') as usize) + (((computer[0] - b'a') as usize) * 32)
}

#[allow(dead_code)]
fn id_to_computer(id: usize) -> [u8; 2] {
    let mut res = [b'a'; 2];
    res[1] += (id & MASK) as u8;
    res[0] += ((id >> 5) & MASK) as u8;
    res
}

fn starts_with_t(id: usize) -> bool {
    (id >> 5) & MASK == (b't' - b'a') as usize
}

fn pair_to_id(lhs: usize, rhs: usize) -> usize {
    lhs.min(rhs) * MAX_ID + lhs.max(rhs)
}

fn run(input: &str) -> usize {
    let bytes = input.as_bytes();
    let mut cur = 0;
    let mut connections = ArrayBitSet::<{ bitset_size(MAX_PAIR) }>::new();
    let mut not_chiefs_set = ArrayBitSet::<{ bitset_size(MAX_ID) }>::new();
    let mut not_chiefs = Vec::new();
    let mut chiefs_set = ArrayBitSet::<{ bitset_size(MAX_ID) }>::new();
    let mut chiefs = Vec::new();
    while cur + 4 < bytes.len() {
        let lhs = computer_to_id(&bytes[cur..cur + 2]);
        cur += 3;
        let rhs = computer_to_id(&bytes[cur..cur + 2]);
        connections.set(pair_to_id(lhs, rhs));
        if !not_chiefs_set.test(lhs) {
            not_chiefs.push(lhs);
            not_chiefs_set.set(lhs);
        }
        if starts_with_t(lhs) && !chiefs_set.test(lhs) {
            chiefs.push(lhs);
            chiefs_set.set(lhs);
        }
        if !not_chiefs_set.test(rhs) {
            not_chiefs.push(rhs);
            not_chiefs_set.set(rhs);
        }
        if starts_with_t(rhs) && !chiefs_set.test(rhs) {
            chiefs.push(rhs);
            chiefs_set.set(rhs);
        }
        cur += 3;
    }
    let mut res = 0;
    for c in chiefs {
        for (i, &l) in not_chiefs.iter().enumerate() {
            if (!starts_with_t(l) || l > c) && connections.test(pair_to_id(c, l)) {
                for &r in &not_chiefs[i + 1..] {
                    if (!starts_with_t(r) || r > c)
                        && connections.test(pair_to_id(c, r))
                        && connections.test(pair_to_id(l, r))
                    {
                        res += 1;
                    }
                }
            }
        }
    }
    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"),
            7
        )
    }
}
