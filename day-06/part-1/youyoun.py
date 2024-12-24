from tool.runners.python import SubmissionPy

def init_problem(s):
    map_ = set()
    pos = None
    lines= s.splitlines()
    n, m = len(lines), len(lines[0])
    for i, l in enumerate(lines):
        for j, c in enumerate(l):
            if c == "^":
                pos = (i, j)
            if c == "#":
                map_.add((i, j))
    return map_, pos, n, m

def get_visited_places(map_, pos, n, m):
    visited = {pos}
    direction = (-1, 0)
    while True:
        while pos not in map_ and  0 <= pos[0] < n and 0 <= pos[1] < m:
            visited.add(pos)
            pos = (pos[0] + direction[0], pos[1] + direction[1])
        if pos[0] >= n or pos[1] >= m or pos[0] < 0 or pos[1] < 0:
            break
        pos = (pos[0] - direction[0], pos[1] - direction[1])
        direction = (direction[1], -direction[0])
    return visited

class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        map_, pos, n, m = init_problem(s)
        visited = get_visited_places(map_, pos, n, m)
        return len(visited)


def test_youyoun():
    """
    Run `python -m pytest ./day-06/part-1/youyoun.py` to test the submission.
    """
    assert (
        YouyounSubmission().run(
            """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""".strip()
        )
        == 41
    )

def test_straight():
    assert (
            YouyounSubmission().run(
                """.
.
.
.
.
.
.
.
^""".strip()
            )
            == 9
    )

def test_round():
    assert (
            YouyounSubmission().run(
                """#.
.#
..
..
..
..
..
..
^.""".strip()
            )
            == 8
    )