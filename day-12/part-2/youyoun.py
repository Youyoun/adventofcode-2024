from collections import defaultdict

from tool.runners.python import SubmissionPy

CORNER_DIRECTIONS = [
    ((-1, 0), (0, 1), (-1, 1)),  # t, r, tr
    ((-1, 0), (0, -1), (-1, -1)),  # t, l, tl
    ((1, 0), (0, -1), (1, -1)),  # b, l, bl
    ((1, 0), (0, 1), (1, 1))  # b, r, br
]


def get_adjacent_4(coord):
    return [
        (coord[0] + 1, coord[1]),
        (coord[0] - 1, coord[1]),
        (coord[0], coord[1] + 1),
        (coord[0], coord[1] - 1),
    ]

def connected_components(coords: set[tuple[int, int]]) -> list[set[tuple[int, int]]]:
    label_to_coords = defaultdict(set)
    already_labeled = set()
    current_label = 0
    while len(already_labeled) != len(coords):
        queue = {next(iter(coords - already_labeled))}
        while len(queue) > 0:
            ele = queue.pop()
            nbs = set(get_adjacent_4(ele)) | {ele}
            for nb in nbs:
                if nb in coords and nb not in already_labeled:
                    label_to_coords[current_label].add(nb)
                    queue.add(nb)
                    already_labeled.add(nb)
        current_label += 1
    return list(label_to_coords.values())


def compute_number_sides(coords: set[tuple[int, int]]) -> int:
    n_corners = 0
    for coord in coords:
        for d in CORNER_DIRECTIONS:
            coord_side_1 = (coord[0] + d[0][0], coord[1] + d[0][1]) not in coords
            coord_side_2 = (coord[0] + d[1][0], coord[1] + d[1][1]) not in coords
            coord_diag = (coord[0] + d[2][0], coord[1] + d[2][1]) not in coords
            n_corners += int(
                coord_side_1 and coord_side_2 or not coord_side_1 and not coord_side_2 and coord_diag
            )
    return n_corners



def parse_coords(s):
    plant_to_coord = defaultdict(set)
    for i, l in enumerate(s.splitlines()):
        for j, plant in enumerate(l):
            plant_to_coord[plant].add((i, j))
    return plant_to_coord


class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        plant_to_coord = parse_coords(s)
        price = 0
        for plant in plant_to_coord:
            for cluster in connected_components(plant_to_coord[plant]):
                area = len(cluster)
                n_sides = compute_number_sides(cluster)
                price += area * n_sides
        return price


def test_youyoun():
    """
    Run `python -m pytest ./day-12/part-1/youyoun.py` to test the submission.
    """
    assert (
            YouyounSubmission().run(
                """AAAA
BBCD
BBCC
EEEC""".strip()
            )
            == 80
    )


def test_example_2():
    assert YouyounSubmission().run("""RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""".strip()) == 1206
