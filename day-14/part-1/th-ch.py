from tool.runners.python import SubmissionPy
from math import prod


class ThChSubmission(SubmissionPy):
    def run(self, s: str, w=101, h=103, seconds=100):
        """
        :param s: input in string format
        :return: solution flag
        """
        robots = {}
        for i, line in enumerate(s.split("\n")):
            p, v = [p[2:].split(",") for p in line.split()]
            robots[i] = ((int(p[0]), int(p[1])), (int(v[0]), int(v[1])))

        for _ in range(seconds):
            for robot, (p, v) in robots.items():
                new_p = ((p[0] + v[0]) % w, (p[1] + v[1]) % h)
                robots[robot] = (new_p, v)

        quadrants = [0, 0, 0, 0]
        for (x, y), _ in robots.values():
            if x < w // 2:
                if y < h // 2:
                    quadrants[0] += 1
                elif y > h // 2:
                    quadrants[2] += 1
            elif x > w // 2:
                if y < h // 2:
                    quadrants[1] += 1
                elif y > h // 2:
                    quadrants[3] += 1

        return prod(quadrants)


def test_th_ch():
    """
    Run `python -m pytest ./day-14/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
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
            w=11,
            h=7,
        )
        == 12
    )
