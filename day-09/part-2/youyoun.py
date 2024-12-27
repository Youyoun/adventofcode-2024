from tool.runners.python import SubmissionPy

def decoded_to_str(decoded, ids):
    str_ = ""
    for i in range(len(decoded)):
        str_ += "".join([str(ids[i]) for _ in range(decoded[i])])
    return str_.replace("-1", ".")

class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        decoded = list(map(int, list(s.strip())))
        ids = [i // 2 if i % 2 == 0 else -1 for i in range(len(decoded))]
        j = len(decoded) - 1
        while j > 0:
            if j % 2 == 1:
                j -= 1
                continue
            span = decoded[j]  # File space
            for i in range(len(decoded)):
                if i % 2 == 0:
                    continue
                free_space = decoded[i]
                if free_space >= span and i < j:
                    file_id = ids[j]
                    ids[j] = -1
                    ids = ids[:i + 1] + [file_id, -1] + ids[i + 1:]
                    decoded = decoded[:i] + [-1, decoded[j], free_space - span] + decoded[i + 1:]
                    decoded[j+2] = -1
                    decoded[j+1] = span + decoded[j+1]
                    j+=1
                    break
            j -= 1
        checksum = 0
        j = 0
        for i in range(len(decoded)):
            if ids[i] == -1:
                if decoded[i] == -1:
                    continue
                j += decoded[i]
                continue
            for k in range(j,j+decoded[i]):
                checksum += ids[i] * k
            j = j+decoded[i]
        return checksum


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
