from typing import OrderedDict
from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        disk = list(map(int, s))

        # build disk map
        start_idx = 0
        blocks = {}  # index in input -> start index in disk
        spaces = OrderedDict()  # index in input -> (start index in disk, size)
        for i, block_size in enumerate(disk):
            if i % 2 == 0:
                blocks[i] = start_idx
            else:
                spaces[i] = (start_idx, block_size)
            start_idx += block_size

        # move blocks
        last_block_idx = len(disk) - 2 if len(disk) % 2 == 0 else len(disk) - 1
        for i in range(last_block_idx, -1, -2):
            block_size = disk[i]
            for start_idx, (start, space_size) in spaces.items():
                if start >= blocks[i]:
                    # could not find a space for this block
                    break
                if space_size >= block_size:
                    # available space to move the block
                    spaces[start_idx] = (start + block_size, space_size - block_size)
                    if space_size == block_size:
                        del spaces[start_idx]
                    blocks[i] = start
                    break

        # compute checksum
        checksum = 0
        for i, start_idx in sorted(blocks.items(), key=lambda x: x[1]):
            block_size = disk[i]
            for j in range(start_idx, start_idx + block_size):
                checksum += j * (i // 2)
        return checksum


"""
00...111...2...333.44.5555.6666.777.888899
0099.111...2...333.44.5555.6666.777.8888..
0099.1117772...333.44.5555.6666.....8888..
0099.111777244.333....5555.6666.....8888..
00992111777.44.333....5555.6666.....8888..
"""


def test_thomren():
    """
    Run `python -m pytest ./day-09/part-2/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
2333133121414131402
""".strip()
        )
        == 2858
    )
