from tool.runners.python import SubmissionPy

from collections import defaultdict
from itertools import combinations


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        antennas = defaultdict(set)
        for y, line in enumerate(s.splitlines()):
            for x, c in enumerate(line):
                if c != ".":
                    antennas[c].add((x, y))
        w, h = x + 1, y + 1

        antinodes = set()
        for antenna in antennas:
            for (x1, y1), (x2, y2) in combinations(antennas[antenna], 2):
                for ax, ay in (2 * x1 - x2, 2 * y1 - y2), (2 * x2 - x1, 2 * y2 - y1):
                    if 0 <= ax < w and 0 <= ay < h:
                        antinodes.add((ax, ay))

        ## Print the grid
        # grid = [list(line) for line in s.splitlines()]
        # for y in range(h):
        #     for x in range(w):
        #         if (x, y) in antinodes:
        #             grid[y][x] = "#"
        # print("\n".join("".join(line) for line in grid))

        return len(antinodes)


def test_th_ch():
    """
    Run `python -m pytest ./day-08/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""".strip()
        )
        == 14
    )
