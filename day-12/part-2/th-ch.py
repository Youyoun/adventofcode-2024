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
            nb_corners = 0  # number of sides == number of corners
            for x, y in region:
                left = (x - 1, y) not in region
                right = (x + 1, y) not in region
                top = (x, y - 1) not in region
                bottom = (x, y + 1) not in region

                top_left = (x - 1, y - 1) not in region
                top_right = (x + 1, y - 1) not in region
                bottom_left = (x - 1, y + 1) not in region
                bottom_right = (x + 1, y + 1) not in region

                corners = sum(
                    [top and right, top and left, bottom and left, bottom and right]
                ) + sum(
                    [
                        not top and not left and top_left,
                        not top and not right and top_right,
                        not bottom and not left and bottom_left,
                        not bottom and not right and bottom_right,
                    ]
                )
                nb_corners += corners

            return nb_corners

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
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
""".strip()
        )
        == 368
    )

    assert (
        ThChSubmission().run(
            """
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
""".strip()
        )
        == 236
    )
