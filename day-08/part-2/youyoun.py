import itertools
import operator
from collections import defaultdict

from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        nodes = defaultdict(list)
        lines = s.splitlines()
        N = len(lines)
        for x, l in enumerate(lines):
            for y, c in enumerate(l):
                if c != '.':
                    nodes[c].append((x, y))
        antinodes = set()
        for freq in nodes:
            for p1, p2 in itertools.combinations(nodes[freq], r=2):
                antinodes.add(p1)
                dx, dy = p2[0] - p1[0], p2[1] - p1[1]
                for op in [operator.add, operator.sub]:
                    an = op(p1[0], dx), op(p1[1], dy)
                    while 0 <= an[0] < N and 0 <= an[1] < N:
                        antinodes.add(an)
                        an = op(an[0], dx), op(an[1], dy)
        return len(antinodes)


def test_youyoun():
    """
    Run `python -m pytest ./day-08/part-1/youyoun.py` to test the submission.
    """
    assert (
            YouyounSubmission().run(
                """............
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
............""".strip()
            )
            == 34
    )


def test_T():
    """
    Run `python -m pytest ./day-08/part-1/youyoun.py` to test the submission.
    """
    assert (
            YouyounSubmission().run(
                """T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........""".strip()
            )
            == 9
    )
