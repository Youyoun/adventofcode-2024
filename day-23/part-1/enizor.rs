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

fn id_to_computer(id: usize) -> [u8; 2] {
    let mut res = [b'a'; 2];
    res[1] += (id & MASK) as u8;
    res[0] += ((id >> 5) & MASK) as u8;
    res
}

fn start_with_t(id: usize) -> bool {
    (id >> 5) & MASK == (b't' - b'a') as usize
}

fn pair_to_id(lhs: usize, rhs: usize) -> usize {
    lhs * MAX_ID + rhs
}

fn run(input: &str) -> usize {
    let bytes = input.as_bytes();
    let mut cur = 0;
    let mut connections = ArrayBitSet::<{ bitset_size(MAX_PAIR) }>::new();
    let mut computers = ArrayBitSet::<{ bitset_size(MAX_ID) }>::new();
    while cur + 4 < bytes.len() {
        let lhs = computer_to_id(&bytes[cur..cur + 2]);
        cur += 3;
        let rhs = computer_to_id(&bytes[cur..cur + 2]);
        connections.set(pair_to_id(lhs.min(rhs), lhs.max(rhs)));
        computers.set(lhs);
        computers.set(rhs);
        cur += 3;
    }
    let mut res = 0;
    for l in 0..MAX_ID {
        if computers.test(l) {
            for r in l + 1..MAX_ID {
                if computers.test(r) && connections.test(pair_to_id(l, r)) {
                    for t in r + 1..MAX_ID {
                        if computers.test(t)
                            && connections.test(pair_to_id(r, t))
                            && connections.test(pair_to_id(l, t))
                            && (start_with_t(l) || start_with_t(r) || start_with_t(t))
                        {
                            // eprintln!(
                            //     "{}-{}-{}",
                            //     core::str::from_utf8(&id_to_computer(l)).unwrap(),
                            //     core::str::from_utf8(&id_to_computer(r)).unwrap(),
                            //     core::str::from_utf8(&id_to_computer(t)).unwrap()
                            // );
                            let ids = [l, r, t];
                            let com: [_; 3] = core::array::from_fn(|i| id_to_computer(ids[i]));
                            let con: [_; 3] =
                                core::array::from_fn(|i| core::str::from_utf8(&com[i]).unwrap());
                            let c1 = [
                                format!("{}-{}", con[0], con[1]),
                                format!("{}-{}", con[1], con[0]),
                            ];
                            assert!((start_with_t(l) || start_with_t(r) || start_with_t(t)));
                            assert!(l < r);
                            assert!(r < t);
                            assert!(l < t);
                            assert!(connections.test(pair_to_id(l, r)));
                            assert!(connections.test(pair_to_id(r, t)));
                            assert!(connections.test(pair_to_id(l, t)));
                            assert!(
                                input.contains(&c1[0]) || input.contains(&c1[1]),
                                "fail 1 for {} {} {} = {} {} {}",
                                con[0],
                                con[1],
                                con[2],
                                ids[0],
                                ids[1],
                                ids[2]
                            );
                            let c2 = [
                                format!("{}-{}", con[1], con[2]),
                                format!("{}-{}", con[2], con[1]),
                            ];
                            assert!(
                                input.contains(&c2[0]) || input.contains(&c2[1]),
                                "fail 2 for {} {} {} = {} {} {}",
                                con[0],
                                con[1],
                                con[2],
                                ids[0],
                                ids[1],
                                ids[2]
                            );
                            let c3 = [
                                format!("{}-{}", con[0], con[2]),
                                format!("{}-{}", con[2], con[0]),
                            ];
                            assert!(
                                input.contains(&c3[0]) || input.contains(&c3[1]),
                                "fail 3 for {} {} {} = {} {} {}",
                                con[0],
                                con[1],
                                con[2],
                                ids[0],
                                ids[1],
                                ids[2]
                            );
                            res += 1;
                        }
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
