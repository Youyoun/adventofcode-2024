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
                f = 2
                while True:
                    ax, ay = (f * x1 - (f - 1) * x2, f * y1 - (f - 1) * y2)
                    if 0 <= ax < w and 0 <= ay < h:

                        antinodes.add((ax, ay))
                    else:
                        break
                    f += 1

                f = 2
                while True:
                    ax, ay = (f * x2 - (f - 1) * x1, f * y2 - (f - 1) * y1)
                    if 0 <= ax < w and 0 <= ay < h:
                        antinodes.add((ax, ay))
                    else:
                        break
                    f += 1

        ## Print the grid
        # grid = [list(line) for line in s.splitlines()]
        # for y in range(h):
        #     for x in range(w):
        #         if (x, y) in antinodes:
        #             grid[y][x] = "#"
        # print("\n".join("".join(line) for line in grid))

        resonant_antennas = set().union(
            *[positions for positions in antennas.values() if len(positions) >= 2]
        )
        return len(antinodes | resonant_antennas)


def test_th_ch():
    """
    Run `python -m pytest ./day-08/part-2/th-ch.py` to test the submission.
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
        == 34
    )
