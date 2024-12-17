use std::env::args;
use std::time::Instant;

use aoc::enizor::parser::Parser;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const ADV: u8 = 0;
const BXL: u8 = 1;
const BST: u8 = 2;
const JNZ: u8 = 3;
const BXC: u8 = 4;
const OUT: u8 = 5;
const BDV: u8 = 6;
const CDV: u8 = 7;

#[derive(Default, Debug, Clone)]
struct Computer<'a> {
    regs: [usize; 3],
    output: String,
    program: &'a [u8],
    ip: usize,
}

impl Computer<'_> {
    fn combo(&self, i: u8) -> usize {
        match i {
            0..4 => i as usize,
            4..7 => self.regs[i as usize - 4],
            7 => panic!("reserved operand!"),
            _ => panic!("unknown operand!"),
        }
    }
    fn run_once(&mut self) -> bool {
        if self.ip + 2 >= self.program.len() {
            return false;
        }
        let i = self.program[self.ip] - b'0';
        let operand = self.program[self.ip + 2] - b'0';
        debug_assert!(i <= 7);
        self.ip += 4;
        match i {
            ADV => self.regs[0] >>= self.combo(operand),
            BXL => self.regs[1] ^= operand as usize,
            BST => self.regs[1] = self.combo(operand) % 8,
            JNZ => {
                if self.regs[0] != 0 {
                    self.ip = 2 * (operand as usize);
                }
            }
            BXC => self.regs[1] ^= self.regs[2],
            OUT => {
                if !self.output.is_empty() {
                    self.output.push(',');
                }
                self.output
                    .push(((self.combo(operand) % 8) as u8 + b'0') as char);
            }
            BDV => self.regs[1] = self.regs[0] >> self.combo(operand),
            CDV => self.regs[2] = self.regs[0] >> self.combo(operand),
            _ => panic!("unknown opcode!"),
        }
        true
    }
    fn run(mut self) -> String {
        while self.run_once() {}
        self.output
    }
    fn new(input: &str) -> Computer<'_> {
        let bytes = input.as_bytes();
        let mut p = Parser::from_input(&bytes);
        let mut regs = [0; 3];
        p.cur = 12;
        regs[0] = p.parse_usize().expect("failed to parse input");
        p.cur += 13;
        regs[1] = p.parse_usize().expect("failed to parse input");
        p.cur += 13;
        regs[2] = p.parse_usize().expect("failed to parse input");
        p.cur += 11;
        Computer {
            regs,
            output: String::new(),
            program: &bytes[p.cur..],
            ip: 0,
        }
    }
}

fn run(input: &str) -> String {
    Computer::new(input).run()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let mut c = Computer {
            regs: [0, 0, 9],
            program: "2,6".as_bytes(),
            ..Default::default()
        };
        assert!(c.run_once());
        assert_eq!(c.regs[1], 1);
        let c = Computer {
            regs: [10, 0, 0],
            program: "5,0,5,1,5,4".as_bytes(),
            ..Default::default()
        };
        assert_eq!(c.run(), "0,1,2");
        let c = Computer {
            regs: [2024, 0, 0],
            program: "0,1,5,4,3,0".as_bytes(),
            ..Default::default()
        };
        assert_eq!(c.run(), "4,2,5,6,7,7,7,7,3,1,0");
        let mut c = Computer {
            regs: [0, 29, 0],
            program: "1,7".as_bytes(),
            ..Default::default()
        };
        c.run_once();
        assert_eq!(c.regs[1], 26);
        let mut c = Computer {
            regs: [0, 2024, 43690],
            program: "4,0".as_bytes(),
            ..Default::default()
        };
        c.run_once();
        assert_eq!(c.regs[1], 44354);
        assert_eq!(
            run("Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"),
            "4,6,3,5,6,3,5,2,1,0"
        )
    }
}
