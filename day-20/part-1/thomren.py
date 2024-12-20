from collections import deque
from tool.runners.python import SubmissionPy

CHEAT_DURATION = 2


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str, min_save: int = 100):
        """
        :param s: input in string format
        :return: solution flag
        """
        maze = [[c for c in line] for line in s.splitlines()]
        start_idx = s.index("S")
        end_idx = s.index("E")
        width = len(maze[0])
        start = (start_idx // (width + 1), start_idx % (width + 1))
        end = (end_idx // (width + 1), end_idx % (width + 1))

        shortest_path = get_shortest_path(maze, start, end)
        dist_from_start = get_distances(maze, start, end)
        dist_from_end = get_distances(maze, end, start)

        res = 0
        for i in range(0, len(shortest_path) - 1):
            x, y = shortest_path[i]
            for dx in range(-CHEAT_DURATION, CHEAT_DURATION + 1):
                for dy in range(
                    -CHEAT_DURATION + abs(dx), CHEAT_DURATION + 1 - abs(dx)
                ):
                    if (
                        0 <= x + dx < len(maze)
                        and 0 <= y + dy < len(maze[0])
                        and maze[x + dx][y + dy] != "#"
                    ):
                        shortest_path_length = (
                            dist_from_start[(x, y)]
                            + abs(dx)
                            + abs(dy)
                            + dist_from_end.get((x + dx, y + dy), float("inf"))
                        )
                        if shortest_path_length <= len(shortest_path) - 1 - min_save:
                            res += 1
        return res


def get_shortest_path(
    maze: list[str],
    start: tuple[int, int],
    end: tuple[int, int],
) -> list[tuple[int, int]] | None:
    queue = deque([start])
    prev = {start: None}
    while queue:
        x, y = queue.popleft()

        if (x, y) == end:
            path = []
            p = (x, y)
            while p is not None:
                path.append(p)
                p = prev[p]
            return path[::-1]

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if (
                not 0 <= x + dx < len(maze)
                or not 0 <= y + dy < len(maze[0])
                or maze[x + dx][y + dy] == "#"
                or (x + dx, y + dy) in prev
            ):
                continue
            prev[(x + dx, y + dy)] = (x, y)
            queue.append((x + dx, y + dy))
    return None


def get_distances(
    maze: list[str],
    start: tuple[int, int],
    end: tuple[int, int],
) -> dict[tuple[int, int], int]:
    queue = deque([start])
    distances = {start: 0}
    while queue:
        x, y = queue.popleft()
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if (
                not 0 <= x + dx < len(maze)
                or not 0 <= y + dy < len(maze[0])
                or maze[x + dx][y + dy] == "#"
                or (x + dx, y + dy) in distances
            ):
                continue
            distances[(x + dx, y + dy)] = distances[(x, y)] + 1
            queue.append((x + dx, y + dy))
    return distances


def test_thomren():
    """
    Run `python -m pytest ./day-20/part-1/thomren.py` to test the submission.
    """
    example_maze = """
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
""".strip()
    assert ThomrenSubmission().run(example_maze, 10) == 10
    assert ThomrenSubmission().run(example_maze, 20) == 5
    assert ThomrenSubmission().run(example_maze, 40) == 2
    assert ThomrenSubmission().run(example_maze, 100) == 0
