from tool.runners.python import SubmissionPy

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        graph = s.splitlines()
        visited = set()
        res = 0
        for i in range(len(graph)):
            for j in range(len(graph[0])):
                if (i, j) in visited:
                    continue
                num_sides = 0
                region_area = 1
                visited.add((i, j))
                stack = [(i, j)]
                while stack:
                    (x, y) = stack.pop()
                    neighbors = []
                    for dx, dy in DIRECTIONS:
                        if (
                            0 <= x + dx < len(graph)
                            and 0 <= y + dy < len(graph[0])
                            and graph[x + dx][y + dy] == graph[x][y]
                        ):
                            neighbors.append((dx, dy))
                            if (x + dx, y + dy) not in visited:
                                stack.append((x + dx, y + dy))
                                visited.add((x + dx, y + dy))
                                region_area += 1

                    # number of sides = number of corners for a polygon
                    # count regular corners
                    if len(neighbors) == 0:
                        num_sides += 4
                    elif len(neighbors) == 1:
                        num_sides += 2
                    elif len(neighbors) == 2 and not (
                        abs(neighbors[0][0]) == abs(neighbors[1][0])
                        and abs(neighbors[0][1]) == abs(neighbors[1][1])
                    ):
                        num_sides += 1

                    # count inverted corners
                    for k in range(4):
                        d1, d2 = DIRECTIONS[k], DIRECTIONS[(k + 1) % 4]
                        if (
                            d1 in neighbors
                            and d2 in neighbors
                            and graph[x + d1[0 + d2[0]]][y + d1[1] + d2[1]]
                            != graph[i][j]
                        ):
                            num_sides += 1
                res += region_area * num_sides
        return res


def test_thomren():
    """
    Run `python -m pytest ./day-12/part-2/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""".strip()
        )
        == 1206
    )
