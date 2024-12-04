from tool.runners.python import SubmissionPy
import re


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        res = 0
        lines = s.splitlines()
        for i in range(len(lines)):
            for j in range(len(lines[0])):
                col = "".join(lines[i + p][j] for p in range(4) if i + p < len(lines))
                row = "".join(
                    lines[i][j + p] for p in range(4) if j + p < len(lines[0])
                )
                diag = "".join(
                    lines[i + p][j + p]
                    for p in range(4)
                    if i + p < len(lines) and j + p < len(lines[0])
                )
                rev_diag = "".join(
                    lines[i + p][j - p]
                    for p in range(4)
                    if i + p < len(lines) and j - p >= 0
                )
                res += sum(
                    int(
                        s
                        in [
                            "XMAS",
                            "SAMX",
                        ]
                    )
                    for s in [col, row, diag, rev_diag]
                )

        return res


def test_thomren():
    """
    Run `python -m pytest ./day-04/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
""".strip()
        )
        == 18
    )
