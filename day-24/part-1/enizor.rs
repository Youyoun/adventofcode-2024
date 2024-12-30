use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

type Num = u32;

const fn str_to_num(s: &[u8]) -> Num {
    let mut res = 0;
    let mut c = 0;
    while c < 3 {
        let b = s[c];
        res *= 36;
        res += match b {
            b'0'..=b'9' => (b - b'0') as Num,
            b'a'..=b'z' => (b - b'a') as Num + 10,
            _ => panic!("invalid wire ID!"),
        };
        c += 1;
    }
    res
}

const ID_SIZE: usize = 10;
const MASK: u32 = (1 << ID_SIZE) - 1;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Op {
    And = 1,
    Or = 2,
    Xor = 3,
}
use Op::*;

#[derive(Debug, Clone, Copy)]
struct Gate {
    lhs: u16,
    rhs: u16,
    op: Op,
}

// a wire is either Set(bool) or unset(Gate(lhs, rhs, op))
#[derive(Debug, Clone, Copy)]
enum Wire {
    Set(bool),
    Gate(Gate),
}

// memory-efficient representation
// First 2 bits: is in SET state, and the bool value
// last 10+10+2=22 bits: lhs, rhs, op
#[derive(Debug, Clone, Copy, Default)]
struct PackedWire {
    packed: u32,
}
const SET_BIT: u32 = 1 << 31;
const SET_VALUE_BIT: u32 = 1 << 30;

impl Gate {
    #[inline(always)]
    fn pack(&self) -> u32 {
        let mut packed = 0;
        debug_assert!(self.lhs < 1 << ID_SIZE);
        packed |= self.lhs as u32;
        packed <<= ID_SIZE;
        debug_assert!(self.rhs < 1 << ID_SIZE);
        packed |= self.rhs as u32;
        packed <<= 2;
        debug_assert!((self.op as u32) < 1 << 2);
        packed |= self.op as u32;
        packed
    }
    #[inline(always)]
    fn unpack(mut packed: u32) -> Self {
        let op = match packed & 0x3 {
            1 => And,
            2 => Or,
            3 => Xor,
            _ => panic!("invalid packed value!"),
        };
        packed >>= 2;
        let rhs = (packed & MASK) as u16;
        packed >>= ID_SIZE;
        let lhs = (packed & MASK) as u16;
        Gate { lhs, rhs, op }
    }
}

impl PackedWire {
    #[inline(always)]
    fn set(&mut self, val: bool) {
        self.packed |= SET_BIT;
        if val {
            self.packed |= SET_VALUE_BIT;
        };
    }
    #[inline(always)]
    fn unpack(&self) -> Wire {
        if self.packed & SET_BIT > 0 {
            Wire::Set(self.packed & SET_VALUE_BIT > 0)
        } else {
            Wire::Gate(Gate::unpack(self.packed))
        }
    }
}

fn fill_grid(wires: &mut [PackedWire], id: u16) -> Option<bool> {
    if id == u16::MAX || wires[id as usize].packed == 0 {
        None
    } else {
        match wires[id as usize].unpack() {
            Wire::Set(val) => Some(val),
            Wire::Gate(gate) => {
                let l = fill_grid(wires, gate.lhs)
                    .unwrap_or_else(|| panic!("failed to construct wire"));
                let r = fill_grid(wires, gate.rhs)
                    .unwrap_or_else(|| panic!("failed to construct wire"));
                let val = match gate.op {
                    And => l & r,
                    Or => l | r,
                    Xor => l ^ r,
                };
                wires[id as usize].set(val);
                Some(val)
            }
        }
    }
}

fn run(input: &str) -> isize {
    let bytes = input.as_bytes();
    let mut cur = 0;
    let mut wires = vec![PackedWire::default(); 512];
    let mut wire_ids = vec![u16::MAX; 36 * 36 * 36];
    let mut max_id = 0;
    // setup inputs
    while cur < bytes.len() {
        if bytes[cur] == b'\n' {
            cur += 1;
            break;
        }
        let num = str_to_num(&bytes[cur..cur + 3]);
        let id = if wire_ids[num as usize] < u16::MAX {
            wire_ids[num as usize]
        } else {
            wire_ids[num as usize] = max_id;
            max_id += 1;
            max_id - 1
        };
        debug_assert_eq!(bytes[cur + 3], b':');
        let val = bytes[cur + 5] == b'1';
        debug_assert!(val || bytes[cur + 5] == b'0');
        wires[id as usize].set(val);
        cur += 7;
    }
    // setup gates
    while cur + 10 < bytes.len() {
        let lhs_num = str_to_num(&bytes[cur..cur + 3]);
        let lhs = if wire_ids[lhs_num as usize] < u16::MAX {
            wire_ids[lhs_num as usize]
        } else {
            wire_ids[lhs_num as usize] = max_id;
            max_id += 1;
            max_id - 1
        };
        let op = match bytes[cur + 4] {
            b'A' => And,
            b'O' => Or,
            b'X' => Xor,
            _ => panic!("unexpected operation!"),
        };
        cur += 7;
        if op != Or {
            cur += 1;
        }
        let rhs_num = str_to_num(&bytes[cur..cur + 3]);
        let rhs = if wire_ids[rhs_num as usize] < u16::MAX {
            wire_ids[rhs_num as usize]
        } else {
            wire_ids[rhs_num as usize] = max_id;
            max_id += 1;
            max_id - 1
        };
        cur += 7;
        let out_num = str_to_num(&bytes[cur..cur + 3]);
        let out = if wire_ids[out_num as usize] < u16::MAX {
            wire_ids[out_num as usize]
        } else {
            wire_ids[out_num as usize] = max_id;
            max_id += 1;
            max_id - 1
        };
        cur += 4;
        let gate = Gate { lhs, rhs, op };
        wires[out as usize].packed = gate.pack();
    }
    let mut num = str_to_num(b"z00");
    let mut shift = 0;
    let mut res = 0;
    for _ten in 0..=9 {
        for _unit in 0..=9 {
            match fill_grid(&mut wires, wire_ids[num as usize]) {
                Some(true) => res |= 1 << shift,
                Some(false) => {}
                None => return res,
            }
            shift += 1;
            num += 1;
        }
        num += 26;
    }
    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"),
            4
        );
        assert_eq!(
            run("x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"),
            2024
        );
    }
}
