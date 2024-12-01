from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        first, second = [], []
        for line in s.splitlines():
            location_ids = line.split()
            first.append(int(location_ids[0]))
            second.append(int(location_ids[1]))

        first.sort()
        second.sort()

        return sum(abs(first[i] - second[i]) for i in range(len(first)))


def test_th_ch():
    """
    Run `python -m pytest ./day-01/part-1/th-ch.py` to test the submission.
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
        == 11
    )
