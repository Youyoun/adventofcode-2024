import itertools

from tool.runners.python import SubmissionPy

SUM = lambda x, y: x + y
PRODUCT = lambda x, y: x * y
CONCAT = lambda x, y: int(str(x) + str(y))


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        res = 0
        for line in s.splitlines():
            test_value, numbers = line.split(": ")
            test_value = int(test_value)
            numbers = tuple([int(n) for n in numbers.split()])
            if self.solve_rec(test_value, numbers):
                res += test_value
        return res

    @classmethod
    def solve_rec(cls, target: int, numbers: tuple[int, ...]) -> bool:
        if len(numbers) == 1:
            return numbers[0] == target
        if numbers[0] > target:
            # the operations can only increase the value, so if we are already above the target, we can stop early
            return False
        for op in [SUM, PRODUCT, CONCAT]:
            x = op(numbers[0], numbers[1])
            if cls.solve_rec(target, (x,) + numbers[2:]):
                return True
        return False


def test_thomren():
    """
    Run `python -m pytest ./day-07/part-2/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".strip()
        )
        == 11387
    )
