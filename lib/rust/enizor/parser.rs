#[derive(Debug, Clone, Copy)]
pub struct Parser<'a> {
    pub bytes: &'a [u8],
    pub cur: usize,
}

impl<'a> Parser<'a> {
    pub fn from_input<T: AsRef<[u8]> + 'a>(input: &'a T) -> Self {
        Self {
            bytes: input.as_ref(),
            cur: 0,
        }
    }
    pub fn eof(&self) -> bool {
        self.cur >= self.bytes.len()
    }
    pub fn parse_usize(&mut self) -> Option<usize> {
        let mut v: Option<usize> = None;
        while self.cur < self.bytes.len() {
            let b = self.bytes[self.cur];
            if b.is_ascii_digit() {
                let val = (b - b'0') as usize;
                v = Some(v.map_or(val, |v| v * 10 + val));
            } else {
                return v;
            }
            self.cur += 1;
        }
        v
    }
    pub fn parse_sized_nb(&mut self, mut size: usize) -> Option<usize> {
        let mut v: Option<usize> = None;
        while self.cur < self.bytes.len() && size > 0 {
            let b = self.bytes[self.cur];
            if b.is_ascii_digit() {
                let val = (b - b'0') as usize;
                v = Some(v.map_or(val, |v| v * 10 + val));
            } else {
                return v;
            }
            self.cur += 1;
            size -= 1;
        }
        v
    }
    pub fn parse_isize(&mut self) -> Option<isize> {
        let neg = self.bytes[self.cur] == b'-';
        if neg {
            self.cur += 1;
        } else if !self.bytes[self.cur].is_ascii_digit() {
            return None;
        }
        let mag = self.parse_usize()? as isize;
        if neg {
            Some(-mag)
        } else {
            Some(mag)
        }
    }
    pub fn find_str(&mut self, needle: &str) -> bool {
        let search_bytes = needle.as_bytes();
        while self.cur < self.bytes.len() {
            if self.bytes[self.cur..].starts_with(search_bytes) {
                self.cur += needle.len();
                return true;
            }
            self.cur += 1;
        }
        false
    }
    pub fn skip_whitespace(&mut self) {
        while self.cur < self.bytes.len() && self.bytes[self.cur].is_ascii_whitespace() {
            self.cur += 1;
        }
    }
    pub fn peek(&mut self) -> Option<&u8> {
        self.bytes.get(self.cur)
    }
}

impl<'a> Iterator for Parser<'a> {
    type Item = &'a u8;

    fn next(&mut self) -> Option<&'a u8> {
        self.cur += 1;
        self.bytes.get(self.cur - 1)
    }
}
