from tool.runners.python import SubmissionPy

from collections import Counter


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        left, right = [], []
        for line in s.splitlines():
            location_ids = line.split()
            left.append(int(location_ids[0]))
            right.append(int(location_ids[1]))

        right = Counter(right)
        return sum(nb * right[nb] for nb in left)


def test_th_ch():
    """
    Run `python -m pytest ./day-01/part-2/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
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
