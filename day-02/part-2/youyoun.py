from tool.runners.python import SubmissionPy


def is_report_safe(numbers):
    sign = None
    for i in range(1, len(numbers)):
        diff = numbers[i] - numbers[i - 1]
        if not 0 < abs(diff) < 4:
            return False
        if sign is None:
            sign = int(diff > 0)
        if sign != int(diff > 0):
            return False
    return True

class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        counts = 0
        for line in s.splitlines():
            init_numbers = list(map(int, line.split()))
            if is_report_safe(init_numbers):
                counts += 1
                continue

            possible_levels = [init_numbers[:i] + init_numbers[i+1:] for i in range(len(init_numbers))]
            for numbers in possible_levels:
                if is_report_safe(numbers):
                    counts += 1
                    break
        return counts


def test_youyoun():
    """
    Run `python -m pytest ./day-02/part-2/youyoun.py` to test the submission.
    """
    assert (
        YouyounSubmission().run(
            """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9""".strip()
        )
        == 4
    )


