from tool.runners.python import SubmissionPy

def init_problem(s):
    map_ = set()
    pos = None
    direction = 0 # U0 R1 D2 L3
    lines= s.splitlines()
    n, m = len(lines), len(lines[0])
    for i, l in enumerate(lines):
        for j, c in enumerate(l):
            if c == "^":
                pos = (i, j)
            if c == "#":
                map_.add((i, j))
    return map_, pos, direction, n, m

def get_visited_places(map_, pos, direction, n, m):
    visited = {pos}
    is_out = False
    while not is_out:
        if direction == 0:
            i = next(i for i in range(pos[0]-1, -2, -1) if (i, pos[1]) in map_ or i==-1)
            visited.update({(i, pos[1]) for i in range(i+1, pos[0])})
            if i == -1:
                is_out=True
                break
            pos = (i+1, pos[1])
            direction = 1
        elif direction == 1:
            j = next(j for j in range(pos[1] + 1, m+1) if (pos[0], j) in map_ or j==m)
            visited.update({(pos[0], j) for j in range(pos[1]+1, j)})
            if j == m:
                is_out = True
                break
            pos = (pos[0], j-1)
            direction = 2
        elif direction==2:
            i = next(i for i in range(pos[0] + 1, n+1) if (i, pos[1]) in map_ or i==n)
            visited.update({(i, pos[1]) for i in range(pos[0]+1, i)})
            if i == n:
                is_out = True
                break
            pos = (i-1, pos[1])
            direction=3
        elif direction==3:
            j = next(j for j in range(pos[1]-1, -2, -1) if (pos[0], j) in map_ or j==-1)
            visited.update({(pos[0], j) for j in range(j+1, pos[1])})
            if j == -1:
                is_out = True
                break
            pos = (pos[0], j+1)
            direction = 0
    return visited

class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        map_, pos, direction, n, m = init_problem(s)
        visited = get_visited_places(map_, pos, direction, n, m)
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