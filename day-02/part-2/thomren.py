from collections import Counter
from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        reports = [list(map(int, line.split())) for line in s.splitlines()]
        return sum(is_safe(report) for report in reports)


def is_safe(levels: list[int], joker: bool = True) -> bool:
    return (
        all(
            levels[i - 1] < levels[i] <= levels[i - 1] + 3
            for i in range(1, len(levels))
        )
        or all(
            levels[i - 1] - 3 <= levels[i] < levels[i - 1]
            for i in range(1, len(levels))
        )
        or (
            joker
            and any(
                is_safe(levels[:i] + levels[i + 1 :], joker=False)
                for i in range(len(levels))
            )
        )
    )


def test_thomren():
    """
    Run `python -m pytest ./day-02/part-2/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""".strip()
        )
        == 4
    )
