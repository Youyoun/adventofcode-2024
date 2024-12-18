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
        frontier = [(0, start, (0, 1))]
        visited = {}
        while frontier:
            dist, pos, direction = heapq.heappop(frontier)
            if (pos, direction) in visited:
                continue
            visited[(pos, direction)] = dist
            if pos == end:
                return dist
            x, y = pos
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                if (
                    maze[x + dx][y + dy] == "#"
                    or ((x + dx, y + dy), (dx, dy)) in visited
                ):
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


def test_thomren():
    """
    Run `python -m pytest ./day-16/part-1/thomren.py` to test the submission.
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
        == 7036
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
        == 11048
    )
