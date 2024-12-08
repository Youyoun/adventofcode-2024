from collections import defaultdict
from itertools import combinations, product

from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        height = len(s.splitlines())
        width = len(s.splitlines()[0])
        antennas = defaultdict(list)
        for x, line in enumerate(s.splitlines()):
            for y, c in enumerate(line):
                if c.isalnum():
                    antennas[c].append((x, y))

        antinodes = set()
        for locations in antennas.values():
            for a1, a2 in product(locations, repeat=2):
                if a1 == a2:
                    continue
                an = (2 * a1[0] - a2[0], 2 * a1[1] - a2[1])
                if 0 <= an[0] < height and 0 <= an[1] < width:
                    antinodes.add(an)
        return len(antinodes)


def test_thomren():
    """
    Run `python -m pytest ./day-08/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
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
