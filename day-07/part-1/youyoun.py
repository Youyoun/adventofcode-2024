import itertools
import operator

from tool.runners.python import SubmissionPy

def parse_equation(eq_str):
    val, numbers = eq_str.split(":")
    val = int(val)
    numbers = list(map(int, numbers.strip().split(" ")))
    return val, numbers

class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        _OPS = [operator.add, operator.mul]
        total_calibration_result = 0
        for eq in s.splitlines():
            test_value, numbers = parse_equation(eq)
            len_ops = len(numbers) - 1
            for ops_combo in itertools.product(_OPS, repeat=len_ops):
                s = numbers[0]
                for i, op in enumerate(ops_combo):
                    s = op(s, numbers[i+1])
                if s == test_value:
                    total_calibration_result += s
                    break
        return total_calibration_result


def test_youyoun():
    """
    Run `python -m pytest ./day-07/part-1/youyoun.py` to test the submission.
    """
    assert (
        YouyounSubmission().run(
            """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20""".strip()
        )
        == 3749
    )
