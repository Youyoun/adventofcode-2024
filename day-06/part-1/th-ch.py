from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        obstacles = set()
        w, h = len(s.split("\n")[0]), len(s.split("\n"))
        for y, line in enumerate(s.split("\n")):
            for x, c in enumerate(line):
                if c == "#":
                    obstacles.add((x, y))
                elif c == "^":
                    guard = (x, y)

        visited = set()
        direction = (0, -1)
        while 0 <= guard[0] < w and 0 <= guard[1] < h:
            while (guard[0] + direction[0], guard[1] + direction[1]) in obstacles:
                direction = (-direction[1], direction[0])
            visited.add(guard)
            guard = (guard[0] + direction[0], guard[1] + direction[1])

        return len(visited)


def test_th_ch():
    """
    Run `python -m pytest ./day-06/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
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
