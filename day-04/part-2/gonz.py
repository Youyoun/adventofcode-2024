import numpy as np

from tool.runners import SubmissionPy


class GonzSubmission(SubmissionPy):
    def run(self, rows: str) -> int:
        rows = rows.strip().split("\n")
        arr = np.array([list(row) for row in rows])
        # Patterns
        base_pattern = np.array([["M", "*", "S"], ["*", "A", "*"], ["M", "*", "S"]])
        patterns = [
            base_pattern,
            base_pattern[:, ::-1],
            base_pattern.T,
            base_pattern.T[::-1],
        ]
        di, dj = base_pattern.shape
        pattern_mask = base_pattern != "*"
        # Count patterns
        count = 0
        for pattern in patterns:
            for i in range(arr.shape[0] - di + 1):
                for j in range(arr.shape[1] - dj + 1):
                    crop = arr[i:i + di, j:j + dj]
                    if np.all(crop[pattern_mask] == pattern[pattern_mask]):
                        count += 1
        return count


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
        == 9
    )
