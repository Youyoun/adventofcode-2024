use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

type Id = u32;

const fn str_to_id(s: &[u8]) -> Id {
    let mut res = 0;
    let mut c = 0;
    while c < 3 {
        let b = s[c];
        res *= 36;
        res += match b {
            b'0'..=b'9' => (b - b'0') as Id,
            b'a'..=b'z' => (b - b'a') as Id + 10,
            _ => panic!("invalid wire ID!"),
        };
        c += 1;
    }
    res
}

fn id_to_str(mut id: Id) -> String {
    let mut res = vec![0; 3];
    for i in 0..3 {
        let c = id % 36;
        res[2 - i] = match c {
            26..36 => c as u8 + b'0',
            0..26 => c as u8 + b'a' - 10,
            _ => panic!("invalid id!"),
        };
        id /= 36;
    }
    String::from_utf8(res).unwrap()
}

const ID_SIZE: usize = std::mem::size_of::<Id>() * 8 - Id::leading_zeros(36 * 36 * 36) as usize;
const MASK: u64 = (1 << ID_SIZE) - 1;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Op {
    And = 1,
    Or = 2,
    Xor = 3,
}
use Op::*;

#[derive(Debug, Clone, Copy)]
struct Gate {
    lhs: Id,
    rhs: Id,
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
// last 18+18+2=38 bits: lhs, rhs, op
#[derive(Debug, Clone, Copy, Default)]
struct PackedWire {
    packed: u64,
}
const SET_BIT: u64 = 1 << 63;
const SET_VALUE_BIT: u64 = 1 << 62;

impl Gate {
    #[inline(always)]
    fn pack(&self) -> u64 {
        let mut packed = 0;
        debug_assert!(self.lhs < 1 << ID_SIZE);
        packed |= self.lhs as u64;
        packed <<= ID_SIZE;
        debug_assert!(self.rhs < 1 << ID_SIZE);
        packed |= self.rhs as u64;
        packed <<= 2;
        debug_assert!((self.op as u64) < 1 << 2);
        packed |= self.op as u64;
        packed
    }
    #[inline(always)]
    fn unpack(mut packed: u64) -> Self {
        let op = match packed & 0x3 {
            1 => And,
            2 => Or,
            3 => Xor,
            _ => panic!("invalid packed value!"),
        };
        packed >>= 2;
        let rhs = (packed & MASK) as Id;
        packed >>= ID_SIZE;
        let lhs = (packed & MASK) as Id;
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

fn fill_grid(wires: &mut [PackedWire], id: Id) -> Option<bool> {
    if wires[id as usize].packed == 0 {
        None
    } else {
        match wires[id as usize].unpack() {
            Wire::Set(val) => Some(val),
            Wire::Gate(gate) => {
                let l = fill_grid(wires, gate.lhs)
                    .unwrap_or_else(|| panic!("failed to construct wire {}", id_to_str(gate.lhs)));
                let r = fill_grid(wires, gate.rhs)
                    .unwrap_or_else(|| panic!("failed to construct wire {}", id_to_str(gate.rhs)));
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
    let mut wires = vec![PackedWire::default(); 36 * 36 * 36];
    // setup inputs
    while cur < bytes.len() {
        if bytes[cur] == b'\n' {
            cur += 1;
            break;
        }
        let id = str_to_id(&bytes[cur..cur + 3]);
        debug_assert_eq!(bytes[cur + 3], b':');
        let val = bytes[cur + 5] == b'1';
        debug_assert!(val || bytes[cur + 5] == b'0');
        wires[id as usize].set(val);
        cur += 7;
    }
    // setup gates
    while cur + 10 < bytes.len() {
        let lhs = str_to_id(&bytes[cur..cur + 3]);
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
        let rhs = str_to_id(&bytes[cur..cur + 3]);
        cur += 7;
        let out = str_to_id(&bytes[cur..cur + 3]);
        cur += 4;
        let gate = Gate { lhs, rhs, op };
        wires[out as usize].packed = gate.pack();
    }
    let mut id = str_to_id(b"z00");
    let mut shift = 0;
    let mut res = 0;
    for _ten in 0..=9 {
        for _unit in 0..=9 {
            match fill_grid(&mut wires, id) {
                Some(true) => res |= 1 << shift,
                Some(false) => {}
                None => return res,
            }
            shift += 1;
            id += 1;
        }
        id += 26;
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
