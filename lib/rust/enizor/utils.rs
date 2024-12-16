pub fn consume_numeral(bytes: &[u8]) -> usize {
    bytes
        .iter()
        .take_while(|b| b.is_ascii_digit())
        .map(|b| (b - b'0') as usize)
        .reduce(|acc, v| acc * 10 + v)
        .unwrap_or(0)
}

/// beat a (t,d) race while pressing for `x ms` iff (time spent travelling)*speed > d
/// <=> `(t-x)x > d`
/// Look at the roots of `-x² + tx -d` :
/// `delta = sqrt(t²-4*d)`
/// R1 = first integer > first root is `floor((t-delta)/2) + 1`
/// R2 = first integer < second root is `ceil((t+delta)/2) -1`
/// number of integers between the roots is `1 + R2 - R1`
/// Cannot find a way to reduce the formula :(
/// Float precision issues: ht + hdelta must be exact when expecting an integer,
/// ht is either .0 or .5 => exact for ht & hdelta < 2^52 => exact for ht < 2^51
/// => t < 2^52
pub fn beat_race(t: f64, d: f64) -> usize {
    debug_assert!(t < (1u64 << 52) as f64);
    let ht = t / 2.;
    let hdelta = (ht * ht - d).sqrt();
    (ht + hdelta).ceil() as usize - 1 - (ht - hdelta).floor() as usize
}

pub fn debug_ascii(bytes: &[u8]) -> String {
    String::from_utf8(bytes.to_vec()).unwrap()
}

pub fn get_2_mut<T>(slice: &mut [T], p1: usize, p2: usize) -> (&mut T, &mut T) {
    assert_ne!(p1, p2);
    assert!(p1 < slice.len());
    assert!(p2 < slice.len());
    if p1 < p2 {
        let (s1, s2) = slice.split_at_mut(p2);
        (&mut s1[p1], &mut s2[0])
    } else {
        let (s1, s2) = slice.split_at_mut(p1);
        (&mut s2[0], &mut s1[p2])
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(consume_numeral(b"11"), 11);
        let mut s = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
        let (x, y) = get_2_mut(&mut s, 4, 7);
        *x += *y;
        let (x, y) = get_2_mut(&mut s, 8, 2);
        *x += *y;
        assert_eq!(s, [0, 1, 2, 3, 11, 5, 6, 7, 10, 9]);
    }
}
