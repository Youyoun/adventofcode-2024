from tool.runners.python import SubmissionPy
from heapq import heapify, heappop, heappush


def find_min_distance_and_shortest_paths(s: str):
    grid = [list(line) for line in s.splitlines()]
    for y in range(len(grid)):
        for x, c in enumerate(grid[y]):
            if c == "S":
                start = (x, y)
            elif c == "E":
                end = (x, y)

    # dijkstra
    visited = {}
    shortest_paths = set()
    min_distance = None
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    pq = [(0, start, (1, 0), {start})]
    heapify(pq)

    def should_visit(direction, x, y, distance):
        current_distance = visited.get(((x, y), direction))
        if current_distance and distance > current_distance:
            return False
        visited[((x, y), direction)] = distance
        return True

    while pq:
        current_distance, (x, y), direction, path = heappop(pq)

        if min_distance and current_distance > min_distance:
            break

        if (x, y) == end:
            min_distance = current_distance
            shortest_paths |= path

        if not should_visit(direction, x, y, current_distance):
            continue

        xx, yy = x + direction[0], y + direction[1]
        if grid[yy][xx] != "#" and should_visit(
            direction, xx, yy, current_distance + 1
        ):
            heappush(
                pq, (current_distance + 1, (xx, yy), direction, path | {(xx, yy)})
            )

        i = directions.index(direction)

        left = directions[(i + 1) % 4]
        if should_visit(left, x, y, current_distance + 1000):
            heappush(pq, (current_distance + 1000, (x, y), left, path))

        right = directions[(i - 1) % 4]
        if should_visit(right, x, y, current_distance + 1000):
            heappush(pq, (current_distance + 1000, (x, y), right, path))

    return min_distance, shortest_paths


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        min_distance, _ = find_min_distance_and_shortest_paths(s)
        return min_distance


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
