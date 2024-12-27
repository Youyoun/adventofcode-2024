from tool.runners.python import SubmissionPy

def decode(disk_map):
    i = 0
    decoded = []
    while i < len(disk_map):
        if i % 2 == 0:
            decoded.extend([i // 2 for _ in range(int(disk_map[i]))])
        else:
            decoded.extend([-1 for _ in range(int(disk_map[i]))])
        i+=1
    return decoded

def decoded_to_str(decoded):
    return "".join(map(str, decoded)).replace("-1", ".")

def move_blocks(decoded):
    i,j = 0, len(decoded)-1
    while i <= j and i < len(decoded) and j >= 0:
        if decoded[i] == -1:
            decoded[i], decoded[j] = decoded[j], decoded[i]
            j -= 1
            while decoded[j] == -1:
                j -= 1
        i+=1
    return decoded

class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        decoded = decode(s.strip())
        moved_blocks = move_blocks(decoded)
        s = 0
        for i in range(len(moved_blocks)):
            if moved_blocks[i] == -1:
                break
            s += i * moved_blocks[i]
        return s




def test_youyoun():
    """
    Run `python -m pytest ./day-09/part-1/youyoun.py` to test the submission.
    """
    assert (
        YouyounSubmission().run(
            """2333133121414131402""".strip()
        )
        == 1928
    )

def test_decode_easy():
    assert decoded_to_str(decode("12345")) == "0..111....22222"

def test_decode():
    assert decoded_to_str(decode("2333133121414131402")) == "00...111...2...333.44.5555.6666.777.888899"

def test_move_blocks():
    assert decoded_to_str(move_blocks(decode("2333133121414131402"))) == "0099811188827773336446555566.............."