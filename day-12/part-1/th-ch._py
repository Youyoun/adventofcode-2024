from tool.runners.python import SubmissionPy
from collections import defaultdict


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        regions = defaultdict(list)
        grid = [list(line) for line in s.splitlines()]
        w, h = len(grid[0]), len(grid)

        def get_region(x, y, c, local_region):
            for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                if (
                    0 <= x + dx < w
                    and 0 <= y + dy < h
                    and grid[y + dy][x + dx] == c
                    and (x + dx, y + dy) not in local_region
                ):
                    local_region.add((x + dx, y + dy))
                    local_region.update(get_region(x + dx, y + dy, c, local_region))
            return local_region

        for y, line in enumerate(grid):
            for x, c in enumerate(line):
                local_region = set([(x, y)])
                local_region = get_region(x, y, c, local_region)
                is_in_existing_region = False
                for region in regions[c]:
                    if region & local_region:
                        region.update(local_region)
                        is_in_existing_region = True
                if not is_in_existing_region:
                    regions[c].append(local_region)

        def get_perimeter(region):
            perimeter = 0
            for x, y in region:
                nb_sides = 4
                for dx, dy in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                    if (x + dx, y + dy) in region:
                        nb_sides -= 1
                perimeter += nb_sides
            return perimeter

        def get_area(region):
            return len(region)

        return sum(
            get_area(region) * get_perimeter(region)
            for region_per_plant in regions.values()
            for region in region_per_plant
        )


def test_th_ch():
    """
    Run `python -m pytest ./day-12/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
""".strip()
        )
        == 772
    )
    assert (
        ThChSubmission().run(
            """
AAAA
BBCD
BBCC
EEEC
""".strip()
        )
        == 140
    )
    assert (
        ThChSubmission().run(
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
