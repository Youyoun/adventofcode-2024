from collections import defaultdict

from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        _sep = "   "
        left = []
        right = defaultdict(int)
        for line in s.split("\n"):
            x, y = map(int, line.split(_sep))
            left.append(x)
            right[y] += 1
        return sum(i * right[i] for i in left)


def test_youyoun():
    """
    Run `python -m pytest ./day-01/part-2/youyoun.py` to test the submission.
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
        == 31
    )
