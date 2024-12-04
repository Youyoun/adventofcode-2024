from tool.runners.python import SubmissionPy

def get(rows: list[str], size: int, row: int, column: int, offset: tuple[int, int], distance: int):
    row_index = row + offset[0] * distance
    if (row_index < 0 or row_index >= size):
        return ""
    column_index = column + offset[1] * distance
    if (column_index < 0 or column_index >= size):
        return ""

    return rows[row_index][column_index]

def count_XMAS_at(rows: list[str], size: int, row: int, column: int):
    if get(rows, size, row, column, (0,0), 0) != 'A':
        return 0

    count = 0

    for offset in ((1,1), (1,-1), (-1,-1), (-1, 1)):
        if get(rows, size, row, column, offset, 1) == "M" and get(rows, size, row, column, (offset[0] * -1, offset[1] * -1), 1) == 'S':
            count += 1

    if count == 2:
        return 1

    return 0

class Ayc0Submission(SubmissionPy):
    def run(self, rows: str) -> int:
        """
        :param rows: input in string format
        :return: solution flag
        """
        count = 0
        rows = rows.strip().split('\n')
        size = len(rows[0])
        for row in range(size):
            for column in range(size):
                count += count_XMAS_at(rows, size, row, column)

        return count


def test_ayc0():
    """
    Run `python -m pytest ./day-04/part-2/ayc0.py` to test the submission.
    """
    assert (
        Ayc0Submission().run(
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
