use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const LENGTH: usize = 5;

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
    if !is_lock {
        for pin in pins.iter_mut() {
            *pin = height - *pin; // maximum pin height accepted by the key
        }
    }
    (pins, is_lock, cur + 1)
}

fn run(input: &str) -> usize {
    let bytes = input.as_bytes();
    let mut cur = 0;
    let mut locks = vec![];
    let mut keys = vec![];
    while cur + 4 < bytes.len() {
        let (pins, is_lock, adv) = parse_schematic(&bytes[cur..]);
        cur += adv;
        if is_lock {
            locks.push(pins);
        } else {
            keys.push(pins);
        }
    }
    let mut res = 0;
    for l in &locks {
        for k in &keys {
            let mut fits = true;
            for i in 0..LENGTH {
                if k[i] < l[i] {
                    fits = false;
                    break;
                }
            }
            if fits {
                res += 1;
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
