from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        _sep = "   "
        left = []
        right = []
        for line in s.split("\n"):
            x, y = map(int, line.split(_sep))
            left.append(x)
            right.append(y)
        return sum(abs(j-i) for i, j in zip(sorted(left), sorted(right)))


def test_youyoun():
    """
    Run `python -m pytest ./day-01/part-1/youyoun.py` to test the submission.
    """
    assert (
        YouyounSubmission().run(
            """3   4
4   3
2   5
1   3
3   9
3   3""".strip()
        )
        == 11
    )