import itertools
from collections import defaultdict

from tool.runners.python import SubmissionPy


def is_point_on_segment(a, b, p):
    return min(b[0], a[0]) <= p[0] <= max(a[0], b[0]) and min(b[1], a[1]) <= p[
        1] <= max(a[1], b[1])


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
                dx, dy = p2[0] - p1[0], p2[1] - p1[1]
                possible_antinodes = [
                    (p2[0] + dx, p2[1] + dy),
                    (p2[0] - dx, p2[1] - dy),
                    (p1[0] + dx, p1[1] + dy),
                    (p1[0] - dx, p1[1] - dy),
                ]
                for an in possible_antinodes:
                    if not is_point_on_segment(p1, p2, an) and 0 <= an[0] < N and 0 <= \
                            an[1] < N:
                        antinodes.add(an)
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
            == 14
    )
