import re
from tool.runners.python import SubmissionPy

def rotate90(s):
    return "\n".join("".join(row) for row in zip(*s.split("\n")[::-1]))

def extract_diagonals(s):
    lines = [line for line in s.split("\n") if line]
    n = len(lines)
    diagonals = []
    anti_diagonals = []

    # Top-left to bottom-right (diagonals)
    for k in range(2*n - 1):
        diag = []
        for i in range(max(0, k - n + 1), min(n, k + 1)):
            j = k - i
            if j < n:
                diag.append(lines[i][j])
        diagonals.append("".join(diag))

    # Top-right to bottom-left (anti-diagonals)
    for k in range(n + n - 1):
        anti_diag = []
        for i in range(max(0, k - n + 1), min(n, k + 1)):
            j = n - 1 - (k - i)
            if j >= 0:
                anti_diag.append(lines[i][j])
        anti_diagonals.append("".join(anti_diag))

    return diagonals + anti_diagonals


class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        regex = [re.compile(r"XMAS"), re.compile(r"SAMX")]
        lines = s.split("\n")
        count = 0
        # Horizontal and vertical
        for reg in regex:
            for line in lines:
                count += len(reg.findall(line))
            for line in rotate90(s).split("\n"):
                count += len(reg.findall("".join(line)))
        # Count diags
        for diag in extract_diagonals(s):
            for reg in regex:
                count += len(reg.findall(diag))
        return count


def test_youyoun():
    """
    Run `python -m pytest ./day-04/part-1/youyoun.py` to test the submission.
    """
    assert (
        YouyounSubmission().run(
            """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".strip()
        )
        == 18
    )
