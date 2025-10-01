from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        # (value, number)
        blocks = [(i // 2 if i % 2 == 0 else None, int(block)) for i, block in enumerate(s)]
        blocks_to_fit = sorted([block for block in blocks if block[0] is not None], key=lambda block: block[0], reverse=True)
        for (file_id, to_fit) in blocks_to_fit:
            index = next(i for i, block in enumerate(blocks) if block[0] == file_id)

            for i, block in enumerate(blocks.copy()):
                if block[0] is not None or i >= index:
                    continue

                if block[0] == file_id:
                    break

                if to_fit <= block[1]:
                    blocks[index] = (None, to_fit)
                    blocks[i] = (None, block[1] - to_fit)
                    blocks.insert(i, (file_id, to_fit))
                    break

            # Compress space blocks
            i = 0
            while i < len(blocks) - 1:
                if blocks[i][0] is None and blocks[i+1][0] is None:
                    blocks[i] = (None, blocks[i][1] + blocks[i+1][1])
                    del blocks[i+1]
                elif blocks[i][0] is None and blocks[i][1] == 0:
                    del blocks[i]
                else:
                    i += 1

        i = 0
        total = 0
        for block in blocks:
            total += sum(block[0] * j for j in range(i, i + block[1]) if block[0] is not None)
            i += block[1]
        return total


def test_th_ch():
    """
    Run `python -m pytest ./day-09/part-2/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
2333133121414131402
""".strip()
        )
        == 2858
    )
