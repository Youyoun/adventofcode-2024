use std::ops::{BitAnd, BitAndAssign, BitOr, BitOrAssign};

#[inline(always)]
pub const fn bitset_size(n: usize) -> usize {
    1 + ((n - 1) / 64)
}

pub type ArrayBitSet<const N: usize> = BitSet<[u64; N]>;

impl<const N: usize> ArrayBitSet<N> {
    #[inline(always)]
    pub fn new() -> Self {
        Self { bits: [0; N] }
    }

    #[inline(always)]
    pub fn ones() -> Self {
        Self { bits: [!0; N] }
    }
}

impl<const N: usize> Default for ArrayBitSet<N> {
    #[inline(always)]
    fn default() -> Self {
        Self::new()
    }
}

pub type VecBitSet = BitSet<Vec<u64>>;

impl VecBitSet {
    #[inline(always)]
    pub fn new(n: impl Into<usize>) -> Self {
        Self {
            bits: vec![0; n.into()],
        }
    }

    #[inline(always)]
    pub fn ones(n: impl Into<usize>) -> Self {
        Self {
            bits: vec![!0; n.into()],
        }
    }
    pub fn ensure_size(&mut self, n: impl Into<usize>) {
        let l = n.into();
        if self.bits.len() < l {
            self.bits.resize(l, 0);
        }
    }
}

pub struct BitSet<T: AsMut<[u64]> + AsRef<[u64]>> {
    pub bits: T,
}

impl<T: Copy + AsMut<[u64]> + AsRef<[u64]>> Copy for BitSet<T> {}

impl<T: Clone + AsMut<[u64]> + AsRef<[u64]>> Clone for BitSet<T> {
    fn clone(&self) -> Self {
        Self {
            bits: self.bits.clone(),
        }
    }
}

impl<T: AsMut<[u64]> + AsRef<[u64]>> BitSet<T> {
    #[inline(always)]
    pub fn test(&self, n: impl Into<usize>) -> bool {
        let p = n.into();
        self.bits.as_ref()[p / 64] & (1 << (p % 64)) > 0
    }

    #[inline(always)]
    pub fn set(&mut self, n: impl Into<usize>) {
        let p = n.into();
        self.bits.as_mut()[p / 64] |= 1 << (p % 64)
    }

    #[inline(always)]
    pub fn reset(&mut self, n: impl Into<usize>) {
        let p = n.into();
        self.bits.as_mut()[p / 64] &= !(1 << (p % 64))
    }

    #[inline(always)]
    pub fn toggle(&mut self, n: impl Into<usize>) {
        let p = n.into();
        self.bits.as_mut()[p / 64] ^= 1 << (p % 64)
    }

    #[inline(always)]
    pub fn count_ones(&self) -> u32 {
        let mut res = 0;
        for &x in self.bits.as_ref() {
            res += x.count_ones();
        }
        res
    }

    #[inline(always)]
    pub fn first_set(&self) -> Option<usize> {
        let mut res = 0;
        for &x in self.bits.as_ref() {
            if x > 0 {
                res += x.trailing_zeros() as usize;
                return Some(res);
            }
            res += 64;
        }
        None
    }
    #[inline(always)]
    pub fn clear(&mut self) {
        for x in self.bits.as_mut() {
            *x = 0;
        }
    }
}

impl<T: AsMut<[u64]> + AsRef<[u64]>> BitAnd<&BitSet<T>> for BitSet<T> {
    type Output = Self;

    #[inline(always)]
    fn bitand(mut self, rhs: &Self) -> Self::Output {
        self &= rhs;
        self
    }
}

impl<T: AsMut<[u64]> + AsRef<[u64]>> BitAndAssign<&BitSet<T>> for BitSet<T> {
    #[inline(always)]
    fn bitand_assign(&mut self, rhs: &BitSet<T>) {
        for i in 0..self.bits.as_ref().len() {
            self.bits.as_mut()[i] &= rhs.bits.as_ref()[i];
        }
    }
}

impl<T: AsMut<[u64]> + AsRef<[u64]>> BitOr<&BitSet<T>> for BitSet<T> {
    type Output = Self;

    #[inline(always)]
    fn bitor(mut self, rhs: &Self) -> Self::Output {
        self |= rhs;
        self
    }
}

impl<T: AsMut<[u64]> + AsRef<[u64]>> BitOrAssign<&BitSet<T>> for BitSet<T> {
    #[inline(always)]
    fn bitor_assign(&mut self, rhs: &Self) {
        for i in 0..self.bits.as_ref().len() {
            self.bits.as_mut()[i] |= rhs.bits.as_ref()[i];
        }
    }
}

/// A 2D-addressable bitset of width W length L
/// with x spanning [W_0 , W + W_O)
/// with y spanning [L_0 , L + W_O)
/// N must be >= bitset_size(L*W)
#[derive(Default)]
pub struct GridBitSet<
    const N: usize,
    const W: usize,
    const W_O: isize,
    const L: usize,
    const L_O: isize,
> {
    pub bitset: ArrayBitSet<N>,
}

impl<const N: usize, const W: usize, const W_O: isize, const L: usize, const L_O: isize>
    GridBitSet<N, W, W_O, L, L_O>
{
    #[inline(always)]
    pub fn new() -> Self {
        debug_assert!(N >= bitset_size(W * L));
        Self {
            bitset: ArrayBitSet::new(),
        }
    }

    #[inline(always)]
    fn pos((x, y): (isize, isize)) -> usize {
        debug_assert!(x - W_O >= 0);
        debug_assert!(W > (x - W_O) as usize);
        debug_assert!(y - L_O >= 0);
        debug_assert!(L > (y - L_O) as usize);
        (y - L_O) as usize * W + (x - W_O) as usize
    }

    #[inline(always)]
    pub fn test(&self, p: (isize, isize)) -> bool {
        self.bitset.test(Self::pos(p))
    }

    #[inline(always)]
    pub fn set(&mut self, p: (isize, isize)) {
        self.bitset.set(Self::pos(p))
    }
    #[inline(always)]
    pub fn reset(&mut self, p: (isize, isize)) {
        self.bitset.reset(Self::pos(p))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let mut set = BitSet::<Vec<u64>>::new(250u8);
        set.set(75u8);
        assert_eq!(set.first_set(), Some(75));
        set.set(36u8);
        assert_eq!(set.first_set(), Some(36));
        set.set(141u8);
        assert_eq!(set.first_set(), Some(36));
        set.reset(36u8);
        assert_eq!(set.first_set(), Some(75));
        set.reset(75u8);
        assert_eq!(set.first_set(), Some(141));
        set.reset(141u8);
        assert_eq!(set.first_set(), None);
    }
}
