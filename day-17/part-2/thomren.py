from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str, return_registers: bool = False):
        """
        :param s: input in string format
        :return: solution flag
        """
        lines = s.splitlines()
        program = [int(x) for x in lines[-1].split(": ")[1].split(",")]
        solutions = {0}
        for out in program[::-1]:
            new_sol = set()
            for x in range(8):
                for sol in solutions:
                    x = out ^ 1 ^ 4 ^ (sol // (2 ** (x + 1)))
                    new_sol.add(sol * 8 + x % 8)
            print(out, solutions)
            solutions = new_sol
        return min(solutions)


def test_thomren():
    """
    Run `python -m pytest ./day-17/part-2/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
""".strip()
        )
        == 117440
    )


"""
2,4 -> B = A % 8
1,1 -> B = B ^ 1
7,5 -> C = A // 2**B
0,3 -> A = A // 8
1,4 -> B = B ^ 4
4,4 -> B = B ^ (A // 2**B)
5,5 -> print(B % 8)
3,0 -> if A != 0: goto 0

"""

B = 2
B = 4
B = 1
B = 1
