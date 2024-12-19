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
        frontier = [(0, start, (0, 1), None)]
        best_dist = None
        optimal_seats = set()
        while frontier:
            dist, pos, direction, path = heapq.heappop(frontier)
            if best_dist and dist > best_dist:
                s = [(end, (0, 1)), (end, (0, -1)), (end, (1, 0)), (end, (-1, 0))]
                visited = set()
                while s:
                    p, d = s.pop()
                    if (p, d) in visited:
                        continue
                    visited.add((p, d))
                    optimal_seats.add(p)
                    if p == start:
                        break
                    s.extend(list(previous[(p, d)]))
                print(sorted(optimal_seats))
                # print(previous)
                return len(optimal_seats)
            if pos == end:
                best_dist = dist
                continue
            x, y = pos
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                if maze[x + dx][y + dy] == "#":
                    continue
                cost = 1 + 1000 * max(abs(dx - direction[0]), abs(dy - direction[1]))
                heapq.heappush(
                    frontier,
                    (dist + cost, (x + dx, y + dy), (dx, dy), direction),
                )


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
