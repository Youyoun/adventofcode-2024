from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        grid = [[c for c in line] for line in s.split("\n")]
        nb_x_mas = 0
        for y in range(len(grid) - 2):
            for x in range(len(grid[y]) - 2):
                if grid[y+1][x+1] != "A":
                    continue

                diag1 = sorted(grid[y][x] + grid[y+2][x+2])
                diag2 = sorted(grid[y][x+2] + grid[y+2][x])
                if diag1 == diag2 == ["M", "S"]:
                    nb_x_mas += 1

        return nb_x_mas



def test_th_ch():
    """
    Run `python -m pytest ./day-04/part-2/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
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
