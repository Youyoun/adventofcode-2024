from tool.runners.python import SubmissionPy
from collections import defaultdict
from heapq import heapify, heappop, heappush


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        grid = [list(line) for line in s.splitlines()]
        G = defaultdict(set)
        start, end = None, None
        for y in range(len(grid)):
            for x, c in enumerate(grid[y]):
                if c == "#":
                    continue
                else:
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        if grid[y + dy][x + dx] != "#":
                            G[(x, y)].add((x + dx, y + dy))
                            G[(x + dx, y + dy)].add((x, y))

                if c == "S":
                    start = (x, y)
                elif c == "E":
                    end = (x, y)

        # dijkstra
        distances = defaultdict(lambda: float("inf"))
        distances[start] = 0
        visited = set()
        pq = [(0, start, (1, 0))]
        heapify(pq)
        while pq:
            current_distance, (x, y), direction = heappop(pq)

            if (x, y) in visited:
                continue
            visited.add((x, y))

            for xx, yy in G[(x, y)]:
                new_direction = (xx - x, yy - y)
                tentative_distance = (
                    current_distance
                    + 1
                    + (
                        abs(new_direction[0] - direction[0])
                        + abs(new_direction[1] - direction[1])
                    )
                    // 2
                    * 1000
                )
                if tentative_distance < distances[(xx, yy)]:
                    distances[(xx, yy)] = tentative_distance
                    heappush(pq, (tentative_distance, (xx, yy), new_direction))

        return distances[end]


def test_th_ch():
    """
    Run `python -m pytest ./day-16/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
""".strip()
        )
        == 7036
    )
