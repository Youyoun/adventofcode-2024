from collections import defaultdict

from sympy.integrals.heurisch import components

from tool.runners.python import SubmissionPy


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


def compute_perimeter(coords: set[tuple[int, int]]) -> int:
    perimeter = 0
    for coord in coords:
        perimeter += sum(adjacent_coord not in coords for adjacent_coord in get_adjacent_4(coord))
    return perimeter


class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        plant_to_coord = defaultdict(set)
        for i, l in enumerate(s.splitlines()):
            for j, plant in enumerate(l):
                plant_to_coord[plant].add((i,j))
        price = 0
        for plant in plant_to_coord:
            for cluster in connected_components(plant_to_coord[plant]):
                area = len(cluster)
                perimeter = compute_perimeter(cluster)
                price += area * perimeter
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
        == 140
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
MMMISSJEEE""".strip()) == 1930