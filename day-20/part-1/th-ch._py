from tool.runners.python import SubmissionPy
from collections import deque
from itertools import combinations


class ThChSubmission(SubmissionPy):
    def run(self, s: str, cheat_length=2, picoseconds_saved=100):
        """
        :param s: input in string format
        :return: solution flag
        """
        grid = [list(line) for line in s.split("\n")]
        source = None

        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == "#":
                    continue
                if grid[y][x] == "S":
                    source = (x, y)

        dist = {source: 0}
        queue = deque([source])
        while queue:
            x, y = queue.popleft()
            for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(grid[y]) and 0 <= ny < len(grid) and grid[ny][nx] != "#" and (nx, ny) not in dist:
                    dist[(nx, ny)] = dist[(x, y)] + 1
                    queue.append((nx, ny))

        cheats = 0
        for ((x1,y1), d1), ((x2,y2), d2) in combinations(dist.items(), 2):
            d = abs(x2 - x1) + abs(y2 - y1)
            if d <= cheat_length and d2 - (d1 + d) >= picoseconds_saved:
                cheats += 1

        return cheats


def test_th_ch():
    """
    Run `python -m pytest ./day-20/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
""".strip(), picoseconds_saved=2
        )
        == 44
    )
