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
        target = [int(x[2:]) + 10000000000000, int(y[2:]) + 10000000000000]
        return coefs, target
