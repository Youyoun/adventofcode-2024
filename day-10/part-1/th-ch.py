from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        G = {}
        grid = [[int(c) for c in line] for line in s.split("\n")]
        w, h = len(grid[0]), len(grid)
        trailheads = []
        for y, line in enumerate(grid):
            for x, height in enumerate(line):
                G[(x, y)] = (height, [])
                if height == 0:
                    trailheads.append((x, y))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if (
                        0 <= x + dx < w
                        and 0 <= y + dy < h
                        and grid[y + dy][x + dx] == height + 1
                    ):
                        G[(x, y)][1].append((x + dx, y + dy))

        def hike(x, y):
            height, neighbors = G[(x, y)]
            if height == 9:
                return set([(x, y)])

            return set().union(*[hike(xx, yy) for xx, yy in neighbors])

        return sum(len(hike(x, y)) for x, y in trailheads)


def test_th_ch():
    """
    Run `python -m pytest ./day-10/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
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
