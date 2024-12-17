use std::env::{self, args};
use std::time::Instant;
use std::{hint, thread};

use aoc::enizor::parser::Parser;
use std::sync::atomic::{AtomicUsize, Ordering};

static GLOBAL_RESULT: AtomicUsize = AtomicUsize::new(0);

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const WIDTH: usize = 101;
const LENGTH: usize = 103;

const DBG_PRINT_DRONES: bool = false;

fn print_drones(drones: &[(usize, usize, usize, usize)]) {
    let mut debug_str = vec![b'.'; (WIDTH + 1) * (LENGTH)];
    for row in 1..=(LENGTH) {
        debug_str[row * (WIDTH + 1) - 1] = b'\n';
    }
    for &(x, y, _, _) in drones {
        debug_str[y * (WIDTH + 1) + x] = b'#';
    }
    eprintln!("{}", String::from_utf8(debug_str).unwrap());
}

/*

A simple christmas tree:

.......
...1...
..111..
.11111.
...1...
.......

can be recognized with long lines of 1
=> if seen as a u128, we get a long set of 1s, probable spanning at least a byte (ensurede if it is as least 15 bits long)
=> that can be checked easily using bitwise operators, see https://graphics.stanford.edu/~seander/bithacks.html#ZeroInWord
*/

// A 1 in the low bit for each byte, i.e. 0x01 repeating
const LOW_BIT: u128 = u128::MAX / 0xFF;
// A 1 in the high bit for each byte, i.e. 0x80 repeating
const HIGH_BIT: u128 = LOW_BIT * 0x80;

fn has_ff(v: u128) -> bool {
    // for each byte, has a set high bit whenever the byte is 0xFF or < 0x80
    let ff_or_not_high_bit = !(v + LOW_BIT);
    // for each byte, has an set high bit whenever the high bit was set in the byte (i.e. >= 0x80)
    let high_bit = v & HIGH_BIT;
    // combining the two gets us the FF bytes presence only
    ff_or_not_high_bit & high_bit > 0
}

fn run_monothread(drones: &mut [(usize, usize, usize, usize)]) -> usize {
    for t in 1..=WIDTH * LENGTH {
        let mut line_count = 0;
        // let mut line_check = [0; LENGTH];
        let mut line_check = [0; LENGTH];
        for (p_x, p_y, v_x, v_y) in drones.iter_mut() {
            *p_x += *v_x;
            if *p_x >= WIDTH {
                *p_x -= WIDTH;
            }
            *p_y += *v_y;
            if *p_y >= LENGTH {
                *p_y -= LENGTH;
            }
            line_check[*p_y] += 1 << *p_x;
        }
        for line in &line_check {
            if has_ff(*line) {
                line_count += 1;
                if line_count >= 4 {
                    if DBG_PRINT_DRONES {
                        eprintln!("\n----- t = {} -----\n", t);
                        print_drones(drones);
                    }
                    return WIDTH * LENGTH - t;
                }
            }
        }
    }
    0
}

fn run_multithread(min: usize, max: usize, drones: &mut [(usize, usize, usize, usize)]) {
    // init: skip `id` turns
    let mut line_count = 0;
    let mut line_check = [0; LENGTH];
    let mut t = min;
    for (p_x, p_y, v_x, v_y) in drones.iter_mut() {
        *p_x += *v_x * min;
        *p_x %= WIDTH;
        *p_y += *v_y * min;
        *p_y %= LENGTH;
        line_check[*p_y] += 1 << *p_x;
    }
    for line in &line_check {
        if has_ff(*line) {
            line_count += 1;
            if line_count >= 4 {
                GLOBAL_RESULT.store(WIDTH * LENGTH - t, Ordering::Release);
                return;
            }
        }
    }
    while t < max {
        t += 1;
        let mut line_count = 0;
        let mut line_check = [0; LENGTH];
        for (p_x, p_y, v_x, v_y) in drones.iter_mut() {
            *p_x += *v_x;
            if *p_x >= WIDTH {
                *p_x -= WIDTH;
            }
            *p_y += *v_y;
            if *p_y >= LENGTH {
                *p_y -= LENGTH;
            }
            line_check[*p_y] |= 1 << *p_x;
        }
        for line in &line_check {
            if has_ff(*line) {
                line_count += 1;
                if line_count >= 4 {
                    GLOBAL_RESULT.store(WIDTH * LENGTH - t, Ordering::Release);
                    return;
                }
            }
        }
        if GLOBAL_RESULT.load(Ordering::Acquire) != 0 {
            break;
        }
    }
}

fn run(input: &str) -> usize {
    let bytes = input.as_bytes();
    let mut drones = Vec::new();
    for line in bytes.split(|&b| b == b'\n') {
        let mut p = Parser::from_input(&line);
        p.cur += 2;
        let p_x = p.parse_usize().expect("failed to parse input");
        p.cur += 1;
        let p_y = p.parse_usize().expect("failed to parse input");
        p.cur += 3;
        let v_x = p
            .parse_isize()
            .map(|v| -v)
            .expect("failed to parse input")
            .rem_euclid(WIDTH as isize) as usize;
        p.cur += 1;
        let v_y = p
            .parse_isize()
            .map(|v| -v)
            .expect("failed to parse input")
            .rem_euclid(LENGTH as isize) as usize;
        drones.push((p_x, p_y, v_x, v_y));
    }
    if DBG_PRINT_DRONES {
        print_drones(&drones);
    }
    let nb_threads = env::var("ENIZOR_DAY_14_NB_THREADS")
        .ok()
        .and_then(|v| v.parse::<usize>().ok())
        .unwrap_or(0);
    if nb_threads < 2 {
        run_monothread(&mut drones)
    } else {
        thread::scope(|s| {
            let mut handles = Vec::new();
            for i in 0..nb_threads - 1 {
                let mut drones2 = drones.clone();
                let block_size = WIDTH * LENGTH / nb_threads + 1;
                handles.push(s.spawn(move || {
                    run_multithread(i * block_size, (i + 1) * block_size, &mut drones2);
                }));
            }
            while GLOBAL_RESULT.load(Ordering::Acquire) == 0 {
                hint::spin_loop();
            }
            GLOBAL_RESULT.load(Ordering::Acquire)
        })
    }
}
