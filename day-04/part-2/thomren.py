from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        res = 0
        lines = s.splitlines()
        for i in range(1, len(lines) - 1):
            for j in range(1, len(lines[0]) - 1):
                diag = lines[i - 1][j - 1] + lines[i][j] + lines[i + 1][j + 1]
                rev_diag = lines[i - 1][j + 1] + lines[i][j] + lines[i + 1][j - 1]
                res += diag in ["MAS", "SAM"] and rev_diag in ["MAS", "SAM"]

        return res


def test_thomren():
    """
    Run `python -m pytest ./day-04/part-2/thomren.py` to test the submission.
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
        == 9
    )
