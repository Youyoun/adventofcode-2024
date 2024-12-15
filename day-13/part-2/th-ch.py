from tool.runners.python import SubmissionPy
from sympy import Matrix
import re


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        machines = s.split("\n\n")

        nb_tokens = 0
        for machine in machines:
            button_a, button_b, prize = machine.split("\n")
            button_a_numbers = re.findall(r"\d+", button_a)
            button_b_numbers = re.findall(r"\d+", button_b)
            prize_numbers = re.findall(r"\d+", prize)

            A = Matrix(
                [
                    [
                        int(button_a_numbers[0]),
                        int(button_b_numbers[0]),
                        -int(prize_numbers[0]) - 10000000000000,
                    ],
                    [
                        int(button_a_numbers[1]),
                        int(button_b_numbers[1]),
                        -int(prize_numbers[1]) - 10000000000000,
                    ],
                ]
            )
            v = A.nullspace()[0]
            if all(nb_times == int(nb_times) for nb_times in [v[0], v[1]]):
                nb_tokens += 3 * v[0] + 1 * v[1]

        return nb_tokens


def test_th_ch():
    """
    Run `python -m pytest ./day-13/part-2/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
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
        == 875318608908
    )
