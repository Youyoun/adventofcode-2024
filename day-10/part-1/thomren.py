from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        topo = [[int(c) for c in line] for line in s.splitlines()]
        res = 0
        for i in range(len(topo)):
            for j in range(len(topo[0])):
                if topo[i][j] != 0:
                    continue
                res += self.find_trails(topo, i, j)
        return res

    @staticmethod
    def find_trails(topo: list[list[int]], x: int, y: int) -> int:
        num_trails = 0
        stack = [(x, y)]
        visited = {(x, y)}
        while stack:
            nx, ny = stack.pop()
            if topo[nx][ny] == 9:
                num_trails += 1
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                if (
                    0 <= nx + dx < len(topo)
                    and 0 <= ny + dy < len(topo[0])
                    and (nx + dx, ny + dy) not in visited
                    and topo[nx + dx][ny + dy] == topo[nx][ny] + 1
                ):
                    stack.append((nx + dx, ny + dy))
                    visited.add((nx + dx, ny + dy))
        return num_trails


def test_thomren():
    """
    Run `python -m pytest ./day-10/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""".strip()
        )
        == 36
    )
