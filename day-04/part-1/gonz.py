import re
from functools import partial
from typing import Sequence

from tool.runners import SubmissionPy


def count_patterns_in_str(line: str, patterns: Sequence[re.Pattern]):
    return sum([len(r.findall(line)) for r in patterns])


class GonzSubmission(SubmissionPy):
    def run(self, rows: str) -> int:
        rows = rows.strip().split('\n')
        # Prepare regex patterns
        words_to_count = ("XMAS", "SAMX")
        patterns = [re.compile(word) for word in words_to_count]
        count_ = partial(count_patterns_in_str, patterns=patterns)
        # Count lines
        line_count = sum([count_(line) for line in rows])
        # Count columns
        columns = ["".join([line[i] for line in rows]) for i in range(len(rows[0]))]
        column_count = sum([count_(column) for column in columns])
        # Count diagonals
        diagonals = []
        for i in range(len(rows)):
            diagonal = "".join([rows[i + j][j] for j in range(len(rows) - i)])
            diagonals.append(diagonal)
        for i in range(1, len(rows)):
            diagonal = "".join([rows[j][i + j] for j in range(len(rows) - i)])
            diagonals.append(diagonal)
        diagonal_count = sum([count_(diagonal) for diagonal in diagonals])
        # Count anti-diagonals
        anti_diagonals = []
        for i in range(len(rows)):
            anti_diagonal = "".join([rows[i - j][j] for j in range(i + 1)])
            anti_diagonals.append(anti_diagonal)
        for i in range(1, len(rows)):
            anti_diagonal = "".join([rows[-1 - j][i + j] for j in range(len(rows) - i)])
            anti_diagonals.append(anti_diagonal)
        anti_diagonal_count = sum(
            [count_(anti_diagonal) for anti_diagonal in anti_diagonals])
        # Compute total count
        total_count = line_count + column_count + diagonal_count + anti_diagonal_count
        return total_count


def test_gonz():
    assert (
        GonzSubmission().run(
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
