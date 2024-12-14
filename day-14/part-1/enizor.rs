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

const TIME: isize = 100;

fn run(input: &str) -> usize {
    const WIDTH: isize = 101;
    const LENGTH: isize = 103;
    let bytes = input.as_bytes();
    let mut quadrants = [0 ; 4];
    for line in bytes.split(|&b| b == b'\n') {
        let mut p = Parser::from_input(&line);
        p.cur+=2;
        let mut p_x = p.parse_isize().expect("failed to parse input");
        p.cur+=1;
        let mut p_y = p.parse_isize().expect("failed to parse input");
        p.cur +=3;
        let v_x = p.parse_isize().expect("failed to parse input");
        p.cur+=1;
        let v_y = p.parse_isize().expect("failed to parse input");
        p_x -= v_x;
        p_x = p_x.rem_euclid(WIDTH);
        p_y -= 3 * v_y;
        p_y= p_y.rem_euclid(LENGTH);

        if p_x != WIDTH / 2 && p_y != LENGTH / 2{
            let mut q = 0;
            q += if p_x < WIDTH / 2 { 0 } else { 1 };
            q += if p_y < LENGTH / 2 { 0 } else { 2 };
            quadrants[q] += 1;
        }

    }
    quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]
}


#[allow(dead_code)]
fn run_small(input: &str) -> usize {
    const WIDTH: isize = 11;
    const LENGTH: isize = 7;
    let bytes = input.as_bytes();
    let mut quadrants = [0 ; 4];
    for line in bytes.split(|&b| b == b'\n') {
        let mut p = Parser::from_input(&line);
        p.cur+=2;
        let mut p_x = p.parse_isize().expect("failed to parse input");
        p.cur+=1;
        let mut p_y = p.parse_isize().expect("failed to parse input");
        p.cur +=3;
        let v_x = p.parse_isize().expect("failed to parse input");
        p.cur+=1;
        let v_y = p.parse_isize().expect("failed to parse input");
        p_x += (TIME % WIDTH) * v_x;
        p_x = p_x.rem_euclid(WIDTH);
        p_y += (TIME % LENGTH)  * v_y;
        p_y= p_y.rem_euclid(LENGTH);

        if p_x != WIDTH / 2 && p_y != LENGTH / 2{
            let mut q = 0;
            q += if p_x < WIDTH / 2 { 0 } else { 1 };
            q += if p_y < LENGTH / 2 { 0 } else { 2 };
            quadrants[q] += 1;
        }

    }
    quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run_small("p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"), 12)
    }
}
