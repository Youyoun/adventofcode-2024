use std::collections::HashMap;
use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn count_ways<'a>(
    design: &'a [u8],
    towels: &[&'a [u8]],
    cache: &mut HashMap<&'a [u8], usize>,
) -> usize {
    if let Some(res) = cache.get(design) {
        *res
    } else {
        let mut p = towels.partition_point(|t| t < &&design[0..1]);
        let p1 = towels.partition_point(|t| t < &[design[0] + 1].as_slice());
        let mut count = 0;
        while p < p1 {
            if design.starts_with(towels[p]) {
                count += count_ways(&design[towels[p].len()..], towels, cache)
            }
            p += 1;
        }
        cache.insert(design, count);
        count
    }
}

fn run(input: &str) -> usize {
    let mut towels = Vec::new();
    let mut cur = 0;
    let bytes = input.as_bytes();
    let mut design_start = 0;
    let mut cache = HashMap::new();
    loop {
        match bytes[cur] {
            b'\n' => {
                towels.push(&bytes[design_start..cur]);
                cur += 2;
                break;
            }
            b',' => {
                towels.push(&bytes[design_start..cur]);
                cur += 2;
                design_start = cur;
            }
            _ => cur += 1,
        }
    }
    cache.insert([].as_slice(), 1);
    towels.sort();
    let mut res = 0;
    while cur < input.len() - 1 {
        let mut next = cur + 1;
        while next < input.len() {
            if bytes[next] == b'\n' {
                break;
            } else {
                next += 1;
            }
        }
        res += count_ways(&bytes[cur..next], &towels, &mut cache);
        cur = next + 1;
    }
    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"),
            16
        )
    }
}
