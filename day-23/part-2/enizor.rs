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

fn pair_to_id(lhs: usize, rhs: usize) -> usize {
    lhs.min(rhs) * MAX_ID + lhs.max(rhs)
}

fn lan_to_string(lan: &[usize], res: &mut String) {
    res.clear();
    res.reserve(lan.len() * 3);
    for id in lan {
        if !res.is_empty() {
            res.push(',');
        }
        for c in id_to_computer(*id) {
            res.push(c as char);
        }
    }
}

fn run(input: &str) -> String {
    let bytes = input.as_bytes();
    let mut cur = 0;
    let mut connections = ArrayBitSet::<{ bitset_size(MAX_PAIR) }>::new();
    let mut computers_set = ArrayBitSet::<{ bitset_size(MAX_ID) }>::new();
    let mut computers = Vec::new();
    while cur + 4 < bytes.len() {
        let lhs = computer_to_id(&bytes[cur..cur + 2]);
        cur += 3;
        let rhs = computer_to_id(&bytes[cur..cur + 2]);
        connections.set(pair_to_id(lhs, rhs));
        if !computers_set.test(lhs) {
            computers.push(lhs);
            computers_set.set(lhs);
        }
        if !computers_set.test(rhs) {
            computers.push(rhs);
            computers_set.set(rhs);
        }
        cur += 3;
    }
    computers.sort_unstable();
    let mut res = String::new();
    let mut lan_len = 0;
    let mut seen_lan = ArrayBitSet::<{ bitset_size(MAX_ID) }>::new();
    for (i, &l) in computers.iter().enumerate() {
        if seen_lan.test(l) {
            continue;
        }
        seen_lan.set(l);
        let mut lan = vec![l];
        for &r in &computers[i + 1..] {
            if seen_lan.test(r) {
                continue;
            }
            let mut in_lan = true;
            for &c in &lan {
                if !connections.test(pair_to_id(c, r)) {
                    in_lan = false;
                    break;
                }
            }
            if in_lan {
                seen_lan.set(r);
                lan.push(r);
            }
        }
        if lan.len() > lan_len {
            lan_to_string(&lan, &mut res);
            lan_len = lan.len();
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
            "co,de,ka,ta"
        )
    }
}
