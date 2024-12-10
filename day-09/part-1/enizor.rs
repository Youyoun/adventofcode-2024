use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let bytes = input.as_bytes();
    let mut res = 0;
    let mut fwd_cur = 0;
    let mut i = 0;
    let mut end_cur = bytes.len() - 1;
    if end_cur % 2 == 1 {
        end_cur -= 1;
    }
    let mut end_countdown = (bytes[end_cur] - b'0') as usize;
    'outer: loop {
        if fwd_cur % 2 == 0 {
            if fwd_cur > end_cur {
                break 'outer;
            }
            let size = if fwd_cur == end_cur {
                // reached the end iterator, only iterate on the few remaining blocks
                end_countdown
            } else {
                (bytes[fwd_cur] - b'0') as usize
            };
            res += fwd_cur * size * (size - 1 + 2 * i) / 4;
            i += size;
        } else {
            let mut empty_space = (bytes[fwd_cur] - b'0') as usize;
            while empty_space > 0 {
                while end_countdown == 0 && end_cur > fwd_cur {
                    end_cur -= 2;
                    end_countdown = (bytes[end_cur] - b'0') as usize;
                }
                if end_cur < fwd_cur {
                    break 'outer;
                }
                let size = end_countdown.min(empty_space);
                res += end_cur * size * (size - 1 + 2 * i) / 4;
                i += size;
                end_countdown -= size;
                empty_space -= size;
            }
        }
        fwd_cur += 1;
    }
    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("2333133121414131402"), 1928);
    }
}
