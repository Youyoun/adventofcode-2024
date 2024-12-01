from tool.runners.python import SubmissionPy


class Ayc0Submission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        left = []
        right = {}
        for line in s.splitlines():
            if not line:
                continue
            a, b = line.split()
            left.append(int(a))
            right[int(b)] = right.get(int(b), 0) + 1

        return sum(a * right.get(a, 0) for a in left)


def test_ayc0():
    """
    Run `python -m pytest ./day-01/part-2/ayc0.py` to test the submission.
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
        == 31
    )
