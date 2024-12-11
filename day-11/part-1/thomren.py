from functools import cache
from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        return sum(solve(int(x), 25) for x in s.split())


@cache
def solve(stone: int, n_iterations: int) -> int:
    if n_iterations == 0:
        return 1
    if stone == 0:
        return solve(1, n_iterations - 1)
    if len(str(stone)) % 2 == 0:
        num_digits = len(str(stone))
        return solve(int(str(stone)[: num_digits // 2]), n_iterations - 1) + solve(
            int(str(stone)[num_digits // 2 :]), n_iterations - 1
        )
    return solve(stone * 2024, n_iterations - 1)


def test_thomren():
    """
    Run `python -m pytest ./day-11/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
125 17
""".strip()
        )
        == 55312
    )
