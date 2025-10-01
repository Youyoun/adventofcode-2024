from tool.runners.python import SubmissionPy

def has_loop(obstacles, w, h, guard):
    visited = set()
    direction = (0, -1)
    while 0 <= guard[0] < w and 0 <= guard[1] < h:
        if (guard, direction) in visited:
            return True
        visited.add((guard, direction))

        while (guard[0] + direction[0], guard[1] + direction[1]) in obstacles:
            direction = (-direction[1], direction[0])
        guard = (guard[0] + direction[0], guard[1] + direction[1])
    return False


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
                    initial_guard = (x, y)

        possible_obstacles = set()
        direction = (0, -1)
        go_right = lambda d: (-d[1], d[0])
        guard = initial_guard
        while True:
            while (guard[0] + direction[0], guard[1] + direction[1]) in obstacles:
                direction = go_right(direction)

            guard = (guard[0] + direction[0], guard[1] + direction[1])
            if 0 <= guard[0] < w and 0 <= guard[1] < h:
                if guard != initial_guard:
                    possible_obstacles.add(guard)
            else:
                break

        nb_loops = 0
        for obstacle in possible_obstacles:
            new_obstacles = obstacles.copy()
            new_obstacles.add(obstacle)
            if has_loop(new_obstacles, w, h, initial_guard):
                nb_loops += 1

        return nb_loops


def test_th_ch():
    """
    Run `python -m pytest ./day-06/part-2/th-ch.py` to test the submission.
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
        == 6
    )
