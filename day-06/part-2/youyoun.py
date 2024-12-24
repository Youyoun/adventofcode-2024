from collections import defaultdict

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

def get_visited_places(map_, pos, n, m, direction):
    visited = defaultdict(set)
    is_loop=False
    iter = 0
    while iter < 5000:
        while pos not in map_ and  0 <= pos[0] < n and 0 <= pos[1] < m:
            pos = (pos[0] + direction[0], pos[1] + direction[1])
            if pos in visited and direction in visited[pos]:
                is_loop=True
                break
            visited[pos].add(direction)
        if pos[0] >= n or pos[1] >= m or pos[0] < 0 or pos[1] < 0:
            break
        pos = (pos[0] - direction[0], pos[1] - direction[1])
        direction = (direction[1], -direction[0])
        iter+=1
    if iter >= 5000:
        print("Iterated too much")
    return visited, is_loop

class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        map_, pos, n, m = init_problem(s)
        visited, is_loop = get_visited_places(map_, pos, n, m, direction=(-1, 0))
        if pos in visited:
            visited.pop(pos)
        loop_counts = 0
        for possible_pos in visited:
            _, is_loop = get_visited_places(map_ | {possible_pos}, pos, n, m, (-1,0))
            loop_counts += int(is_loop)
        return loop_counts


def test_youyoun():
    """
    Run `python -m pytest ./day-06/part-2/youyoun.py` to test the submission.
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
        == 6
    )

def test_loop():
    """
    Run `python -m pytest ./day-06/part-2/youyoun.py` to test the submission.
    """
    s = """.#..
...#
#^..
..#.""".strip()
    map_, pos, n, m = init_problem(s)
    _, is_loop = get_visited_places(map_, pos, n, m, direction=(-1, 0))
    assert is_loop

def test_not_loop():
    """
    Run `python -m pytest ./day-06/part-2/youyoun.py` to test the submission.
    """
    s = """.#..
...#
.^..
..#.""".strip()
    map_, pos, n, m = init_problem(s)
    _, is_loop = get_visited_places(map_, pos, n, m, direction=(-1, 0))
    assert not is_loop