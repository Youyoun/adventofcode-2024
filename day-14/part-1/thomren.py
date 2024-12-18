from functools import reduce
from tool.runners.python import SubmissionPy

import re


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str, width: int = 101, height: int = 103) -> int:
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

        for _ in range(100):
            for i in range(len(positions)):
                x, y = positions[i]
                vx, vy = velocities[i]
                positions[i] = ((x + vx) % width, (y + vy) % height)

        quadrants = [0, 0, 0, 0]
        for pos in positions:
            y, x = pos
            if x < height // 2:
                if y < width // 2:
                    quadrants[0] += 1
                elif y > width // 2:
                    quadrants[1] += 1
            elif x > height // 2:
                if y < width // 2:
                    quadrants[2] += 1
                elif y > width // 2:
                    quadrants[3] += 1
        return reduce(lambda x, y: x * y, quadrants, 1)


def test_thomren():
    """
    Run `python -m pytest ./day-14/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
""".strip(),
            11,
            7,
        )
        == 12
    )
