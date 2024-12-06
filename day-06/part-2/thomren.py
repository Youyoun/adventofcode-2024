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

        initial_path = self.get_initial_path(room, (x, y), (dx, dy))

        res = 0
        room = [list(row) for row in room]
        for x1, y1 in initial_path:
            if not room[x1][y1] == ".":
                continue
            room[x1][y1] = "#"
            res += self.is_loop(room, (x, y), (dx, dy))
            room[x1][y1] = "."
        return res

    @staticmethod
    def get_initial_path(
        room: list[str], p0: tuple[int, int], d0: tuple[int, int]
    ) -> set[tuple[int, int]]:
        x, y = p0
        dx, dy = d0
        visited = {(x, y)}
        while True:
            if 0 <= x + dx < len(room) and 0 <= y + dy < len(room[0]):
                if room[x + dx][y + dy] != "#":
                    x, y = x + dx, y + dy
                    visited.add((x, y))
                else:
                    dx, dy = dy, -dx
            else:
                return visited

    @staticmethod
    def is_loop(room: list[list[str]], p0: tuple[int, int], d0: tuple[int, int]):
        x, y = p0
        dx, dy = d0
        visited = set()
        while True:
            if (x, y, dx, dy) in visited:
                return True
            visited.add((x, y, dx, dy))
            if 0 <= x + dx < len(room) and 0 <= y + dy < len(room[0]):
                if room[x + dx][y + dy] != "#":
                    x, y = x + dx, y + dy
                else:
                    dx, dy = dy, -dx
            else:
                return False


def test_thomren():
    """
    Run `python -m pytest ./day-06/part-2/thomren.py` to test the submission.
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
        == 6
    )
