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
                for k in range(max(height, width)):
                    an = (a1[0] + k * (a1[0] - a2[0]), a1[1] + k * (a1[1] - a2[1]))
                    if not 0 <= an[0] < height or not 0 <= an[1] < width:
                        break
                    antinodes.add(an)
        return len(antinodes)


def test_thomren():
    """
    Run `python -m pytest ./day-08/part-2/thomren.py` to test the submission.
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
        == 34
    )
