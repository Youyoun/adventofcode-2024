import re

from tool.runners.python import SubmissionPy

DIRECTIONS = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        room = s.splitlines()
        guard_idx = re.search(r"[\^v><]", s).start()
        x, y = (guard_idx // (len(room[0]) + 1), guard_idx % (len(room[0]) + 1))
        dx, dy = DIRECTIONS[s[guard_idx]]
        visited = {(x, y)}
        while True:
            if 0 <= x + dx < len(room) and 0 <= y + dy < len(room[0]):
                if room[x + dx][y + dy] != "#":
                    x, y = x + dx, y + dy
                    visited.add((x, y))
                else:
                    dx, dy = dy, -dx
            else:
                return len(visited)


def test_thomren():
    """
    Run `python -m pytest ./day-06/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".strip()
        )
        == 41
    )
