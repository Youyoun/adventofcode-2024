import itertools

from tool.runners.python import SubmissionPy

SUM = lambda x, y: x + y
PRODUCT = lambda x, y: x * y


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
            numbers = [int(n) for n in numbers.split()]
            for operations in itertools.product(
                [SUM, PRODUCT], repeat=len(numbers) - 1
            ):
                if self.evaluate(numbers, operations) == test_value:
                    res += test_value
                    break
        return res

    @staticmethod
    def evaluate(numbers: list[int], operations: list[callable]) -> int:
        res = numbers[0]
        for op, n in zip(operations, numbers[1:]):
            res = op(res, n)
        return res


def test_thomren():
    """
    Run `python -m pytest ./day-07/part-1/thomren.py` to test the submission.
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
        == 3749
    )
