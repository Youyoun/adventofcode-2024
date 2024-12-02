from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        nb_safe = 0
        for report in s.splitlines():
            numbers = list(map(int, report.split()))
            diff = [numbers[i+1] - numbers[i] for i in range(len(numbers) - 1)]
            safe = (all(d >= 0 for d in diff) or all(d <= 0 for d in diff)) and all(1<=abs(d)<=3 for d in diff)
            nb_safe += int(safe)
        return nb_safe


def test_th_ch():
    """
    Run `python -m pytest ./day-02/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""".strip()
        )
        == 2
    )
