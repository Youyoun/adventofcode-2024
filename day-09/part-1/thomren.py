from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        disk = list(map(int, s))
        res = 0
        i = 0
        last_block = 2 * ((len(disk) - 1) // 2)
        last_block_remaining = disk[last_block]
        processed_blocks = set()
        for idx, b in enumerate(disk):
            if idx % 2 == 0:  # block
                if idx in processed_blocks:  # already moved from the end
                    return res
                if idx == last_block:  # block being moved, keep what's left
                    b = last_block_remaining
                    last_block -= 2
                    last_block_remaining = disk[last_block]
                for _ in range(b):  # update checksum
                    res += (idx // 2) * i
                    i += 1
                processed_blocks.add(idx)
            else:  # empty space
                if (
                    last_block in processed_blocks
                ):  # next block to move already processed
                    return res
                for _ in range(b):
                    if last_block_remaining == 0:  # move on to the previous block
                        processed_blocks.add(last_block)
                        last_block -= 2
                        last_block_remaining = disk[last_block]
                    res += (last_block // 2) * i
                    last_block_remaining -= 1
                    i += 1
        return res


def test_thomren():
    """
    Run `python -m pytest ./day-09/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
2333133121414131402
""".strip()
        )
        == 1928
    )
