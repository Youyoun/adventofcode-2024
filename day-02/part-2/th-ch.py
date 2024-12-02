from tool.runners.python import SubmissionPy

def is_safe(numbers):
    diff = [numbers[i+1] - numbers[i] for i in range(len(numbers) - 1)]
    return (all(d >= 0 for d in diff) or all(d <= 0 for d in diff)) and all(1<=abs(d)<=3 for d in diff)


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        nb_safe = 0
        for report in s.splitlines():
            numbers = list(map(int, report.split()))
            if is_safe(numbers):
                nb_safe += 1
                continue

            for i in range(len(numbers)):
                if is_safe(numbers[:i] + numbers[i+1:]):
                    nb_safe += 1
                    break

        return nb_safe


def test_th_ch():
    """
    Run `python -m pytest ./day-02/part-2/th-ch.py` to test the submission.
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
        == 4
    )
