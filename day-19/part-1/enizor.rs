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

fn can_make<'a>(
    design: &'a [u8],
    towels: &[&'a [u8]],
    cache: &mut HashMap<&'a [u8], bool>,
) -> bool {
    if let Some(res) = cache.get(design) {
        *res
    } else {
        let mut p = towels.partition_point(|t| t < &&design[0..1]);
        let p1 = towels.partition_point(|t| t < &[design[0] + 1].as_slice());
        while p < p1 {
            if design.starts_with(towels[p]) && can_make(&design[towels[p].len()..], towels, cache)
            {
                cache.insert(design, true);
                return true;
            }
            p += 1;
        }
        cache.insert(design, false);
        false
    }
}

fn run(input: &str) -> isize {
    let mut towels = Vec::new();
    let mut cur = 0;
    let bytes = input.as_bytes();
    let mut design_start = 0;
    let mut cache = HashMap::new();
    loop {
        match bytes[cur] {
            b'\n' => {
                towels.push(&bytes[design_start..cur]);
                cache.insert(&bytes[design_start..cur], true);
                cur += 2;
                break;
            }
            b',' => {
                towels.push(&bytes[design_start..cur]);
                cache.insert(&bytes[design_start..cur], true);
                cur += 2;
                design_start = cur;
            }
            _ => cur += 1,
        }
    }
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
        if can_make(&bytes[cur..next], &towels, &mut cache) {
            res += 1;
        }
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
            6
        )
    }
}
