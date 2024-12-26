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

def find_empty_space_with_length(decoded, len_):
    for i in range(len_, len(decoded)):
        if sum(decoded[i-len_:i]) == -len_:
            return i - len_
    return None

def move_blocks(decoded):
    j = len(decoded)-1
    while j >= 0:
        while decoded[j] == -1:
            j -= 1
        span_j = j
        while decoded[j] == decoded[span_j]:
            span_j -= 1
        file_len = j - span_j
        i = find_empty_space_with_length(decoded, file_len)
        if i is not None and i < j:
            decoded[i:i+file_len], decoded[span_j+1:j+1] = decoded[span_j+1:j+1], decoded[i:i+file_len]
        j = span_j
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
                continue
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
            == 2858
    )


def test_decode_easy():
    assert decoded_to_str(decode("12345")) == "0..111....22222"


def test_decode():
    assert decoded_to_str(
        decode("2333133121414131402")) == "00...111...2...333.44.5555.6666.777.888899"


def test_move_blocks():
    assert decoded_to_str(move_blocks(
        decode("2333133121414131402"))) == "00992111777.44.333....5555.6666.....8888.."
