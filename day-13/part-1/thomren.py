from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        machines = s.split("\n\n")
        res = 0
        for machine in machines:
            coefs, target = self.parse_machine(machine)
            det = coefs[0][0] * coefs[1][1] - coefs[0][1] * coefs[1][0]
            if det == 0:
                continue
            sol = [
                (coefs[1][1] * target[0] - coefs[0][1] * target[1]) // det,
                (-coefs[1][0] * target[0] + coefs[0][0] * target[1]) // det,
            ]
            if (
                sol[0] >= 0
                and sol[1] >= 0
                and coefs[0][0] * sol[0] + coefs[0][1] * sol[1] == target[0]
                and coefs[1][0] * sol[0] + coefs[1][1] * sol[1] == target[1]
            ):
                res += sol[0] * 3 + sol[1]
        return res

    @staticmethod
    def parse_machine(s: str) -> tuple[list[list[int]], list[int]]:
        coefs = [[0, 0], [0, 0]]
        lines = s.splitlines()
        _, a = lines[0].split(": ")
        x, y = a.split(", ")
        coefs[0][0] = int(x[2:])
        coefs[1][0] = int(y[2:])
        _, b = lines[1].split(": ")
        x, y = b.split(", ")
        coefs[0][1] = int(x[2:])
        coefs[1][1] = int(y[2:])
        _, p = lines[2].split(": ")
        x, y = p.split(", ")
        target = [int(x[2:]), int(y[2:])]
        return coefs, target


def test_thomren():
    """
    Run `python -m pytest ./day-13/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
""".strip()
        )
        == 480
    )
