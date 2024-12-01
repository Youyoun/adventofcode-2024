from tool.runners.python import SubmissionPy


class Ayc0Submission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        left = []
        right = []
        for line in s.splitlines():
            if not line:
                continue
            a, b = line.split()
            left.append(int(a))
            right.append(int(b))

        left.sort()
        right.sort()

        return sum(abs(a - b) for a, b in zip(left, right))


def test_ayc0():
    """
    Run `python -m pytest ./day-01/part-1/ayc0.py` to test the submission.
    """
    assert (
        Ayc0Submission().run(
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
