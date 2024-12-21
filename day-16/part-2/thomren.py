from collections import defaultdict
import heapq
from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        maze = s.splitlines()
        start_idx = s.index("S")
        start = start_idx // (len(maze[0]) + 1), (start_idx % (len(maze[0]) + 1))
        end_idx = s.index("E")
        end = end_idx // (len(maze[0]) + 1), (end_idx % (len(maze[0]) + 1))

        distances_from_start = get_distances(maze, start, (0, 1))
        distances_from_end = get_distances(maze, end, None)
        shortest_path = min(
            distances_from_start.get((end, d), float("inf"))
            for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]
        )

        best_seats = set()
        for p, d in distances_from_start:
            if any(
                distances_from_start[(p, d)]
                + distances_from_end.get((p, d2), float("inf"))
                + 1000 * int(d[0] * d2[0] + d[1] * d2[1] == 0)
                == shortest_path
                for d2 in [(0, 1), (0, -1), (1, 0), (-1, 0)]
            ):
                best_seats.add(p)
        return len(best_seats)


def get_distances(
    maze: list[str], start: tuple[int, int], start_direction: tuple[int, int] | None
) -> dict[tuple[int, int], int]:
    frontier = (
        [(0, start, start_direction)]
        if start_direction
        else [(0, start, d) for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
    )
    distances = {}
    while frontier:
        dist, pos, direction = heapq.heappop(frontier)
        if (pos, direction) in distances:
            continue
        distances[(pos, direction)] = dist
        x, y = pos
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            if maze[x + dx][y + dy] == "#" or ((x + dx, y + dy), (dx, dy)) in distances:
                continue
            cost = 1 + 1000 * max(abs(dx - direction[0]), abs(dy - direction[1]))
            heapq.heappush(
                frontier,
                (
                    dist + cost,
                    (x + dx, y + dy),
                    (dx, dy),
                ),
            )
    return distances


def test_thomren():
    """
    Run `python -m pytest ./day-16/part-2/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
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
        == 45
    )
    assert (
        ThomrenSubmission().run(
            """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
""".strip()
        )
        == 64
    )
