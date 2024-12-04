from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        grid = [[c for c in line] for line in s.split("\n")]
        nb_xmas = 0
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] != "X":
                    continue

                for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
                    xmas_x, xmas_y = x, y
                    contains_xmas = True
                    for letter in "MAS":
                        if (
                            0 <= xmas_x + dx < len(grid[y])
                            and 0 <= xmas_y + dy < len(grid)
                            and grid[xmas_y + dy][xmas_x + dx] == letter
                        ):
                            xmas_x += dx
                            xmas_y += dy
                        else:
                            contains_xmas = False
                            break

                    if contains_xmas:
                        nb_xmas += 1

        return nb_xmas


def test_th_ch():
    """
    Run `python -m pytest ./day-04/part-1/th-ch.py` to test the submission.
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
        == 18
    )
