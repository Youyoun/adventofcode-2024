from tool.runners.python import SubmissionPy


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
                region_perimeter = 0
                region_area = 1
                visited.add((i, j))
                stack = [(i, j)]
                while stack:
                    (x, y) = stack.pop()
                    for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                        if (
                            0 <= x + dx < len(graph)
                            and 0 <= y + dy < len(graph[0])
                            and graph[x + dx][y + dy] == graph[x][y]
                        ):
                            if (x + dx, y + dy) not in visited:
                                stack.append((x + dx, y + dy))
                                visited.add((x + dx, y + dy))
                                region_area += 1
                        else:
                            region_perimeter += 1
                res += region_area * region_perimeter
        return res


def test_thomren():
    """
    Run `python -m pytest ./day-12/part-1/thomren.py` to test the submission.
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
        == 1930
    )
