from tool.runners.python import SubmissionPy
from math import prod
from time import sleep


class ThChSubmission(SubmissionPy):
    def run(self, s: str, w=101, h=103, seconds=100000):
        """
        :param s: input in string format
        :return: solution flag
        """
        robots = {}
        for i, line in enumerate(s.split("\n")):
            p, v = [p[2:].split(",") for p in line.split()]
            robots[i] = ((int(p[0]), int(p[1])), (int(v[0]), int(v[1])))

        current_second = 0
        while True:
            current_second += 1
            for robot, (p, v) in robots.items():
                new_p = ((p[0] + v[0]) % w, (p[1] + v[1]) % h)
                robots[robot] = (new_p, v)

            positions = set([p for p, _ in robots.values()])
            sorted_positions = sorted(positions)
            continuous = 0
            for i in range(len(sorted_positions) - 1):
                if (
                    abs(sorted_positions[i + 1][0] - sorted_positions[i][0])
                    + abs(sorted_positions[i + 1][1] - sorted_positions[i][1])
                    == 1
                ):
                    continuous += 1
                else:
                    continuous = 0
                if continuous > 8:
                    # print(f"------------- {current_second} ------------")
                    # print(
                    #     "\n".join(
                    #         "".join(
                    #             "#" if (x, y) in positions else "." for x in range(w)
                    #         )
                    #         for y in range(h)
                    #     )
                    # )
                    return current_second
