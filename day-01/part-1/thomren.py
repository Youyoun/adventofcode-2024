from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        left, right = [], []
        for line in s.splitlines():
            l, r = line.split()
            left.append(int(l))
            right.append(int(r))
        return sum(abs(l - r) for l, r in zip(sorted(left), sorted(right)))


def test_thomren():
    """
    Run `python -m pytest ./day-01/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
3   4
4   3
2   5
1   3
3   9
3   3
""".strip()
        )
        == 11
    )
