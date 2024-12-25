import math

from tool.runners.python import SubmissionPy

def parse_equation(eq_str):
    val, numbers = eq_str.split(":")
    val = int(val)
    numbers = list(map(int, numbers.strip().split(" ")))
    return val, numbers

def concat(a, b):
    n_digits = int(math.log10(b))+1
    return a * 10 ** n_digits + b

def split(a, b):
    n_digits = int(math.log10(b)) + 1
    return (a - b) // 10 ** n_digits

def mul(a, b):
    return a*b

class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        total_calibration_result = 0
        for eq in s.splitlines():
            test_value, numbers = parse_equation(eq)
            if is_possible(numbers, test_value):
                total_calibration_result += test_value
        return total_calibration_result

def is_possible(numbers: list[int], test_value):
    if len(numbers) == 2:
        return (sum(numbers) == test_value) or mul(*numbers) == test_value or concat(*numbers) == test_value
    sub_path = False
    mul_path = False
    concat_path = False
    if test_value >= numbers[-1]:
        sub_path = is_possible(numbers[:-1], test_value - numbers[-1])
        if test_value % numbers[-1] == 0:
            mul_path = is_possible(numbers[:-1], test_value // numbers[-1])
        if str(test_value).endswith(str(numbers[-1])) :
            concat_path = is_possible(numbers[:-1], split(test_value, numbers[-1]))
    return sub_path or mul_path or concat_path


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
        == 11387
    )