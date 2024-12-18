from math import log
from functools import reduce
from collections import Counter
from tool.runners.python import SubmissionPy

import re


class ThomrenSubmission(SubmissionPy):
    def run(
        self, s: str, width: int = 101, height: int = 103, debug: bool = False
    ) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        positions = []
        velocities = []
        regex = re.compile(r"p=([-\d]+),([-\d]+) v=([-\d]+),([-\d]+)")
        for line in s.splitlines():
            m = regex.match(line)
            positions.append((int(m.group(1)), int(m.group(2))))
            velocities.append((int(m.group(3)), int(m.group(4))))

        for iteration in range(10000):
            for i in range(len(positions)):
                x, y = positions[i]
                vx, vy = velocities[i]
                positions[i] = ((x + vx) % width, (y + vy) % height)
            ex = entropy([p[0] for p in positions])
            ey = entropy([p[1] for p in positions])
            if ex * ey < 17:
                if debug:
                    print(f"{iteration} - {ex * ey} ({ex} - {ey})")
                    print_robots(positions, width, height)
                return iteration + 1


def entropy(values):
    c = Counter(values)
    return sum(-v / len(values) * log(v / len(values)) for v in c.values())


def print_robots(positions: list[tuple[int, int]], width: int, height: int):
    grid = [["." for _ in range(width)] for _ in range(height)]
    for x, y in positions:
        grid[y][x] = "#"
    print("\n".join("".join(row) for row in grid))
