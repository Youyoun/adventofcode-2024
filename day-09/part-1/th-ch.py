from tool.runners.python import SubmissionPy

class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        # (value, number)
        blocks = [(i // 2 if i % 2 == 0 else None, int(block)) for i, block in enumerate(s)]

        last = len(blocks) - 1
        first = 1
        while first < last:
            available_space = blocks[first][1]
            if available_space > blocks[last][1]:
                blocks.insert(first, (blocks[last][0], blocks[last][1]))
                first += 1
                blocks[first] = (blocks[first][0], blocks[first][1] - blocks[last+1][1])
                del blocks[last + 1]
                last -= 1
            elif available_space == blocks[last][1]:
                blocks[first] = (blocks[last][0], available_space)
                first += 2
                del blocks[last]
                last -= 2
            else:
                blocks[first] = (blocks[last][0], available_space)
                blocks[last] = (blocks[last][0], blocks[last][1] - available_space)
                first += 2

        i = 0
        total = 0
        for block in blocks:
            total += sum(block[0] * j for j in range(i, i + block[1]) if block[0] is not None)
            i += block[1]
        return total


def test_th_ch():
    """
    Run `python -m pytest ./day-09/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
2333133121414131402
""".strip()
        )
        == 1928
    )
