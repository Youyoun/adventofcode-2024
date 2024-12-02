from tool.runners.python import SubmissionPy

class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        counts = 0
        for line in s.splitlines():
            numbers = list(map(int, line.split()))
            sign = None
            is_safe = True
            for i in range(1, len(numbers)):
                diff = numbers[i] - numbers[i - 1]
                if not 0 < abs(diff) < 4:
                    is_safe = False
                    break
                if sign is None:
                    sign = int(diff > 0)
                if sign != int(diff > 0):
                    is_safe = False
                    break
            counts += int(is_safe)
        return counts





def test_youyoun():
    """
    Run `python -m pytest ./day-02/part-1/youyoun.py` to test the submission.
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
        == 2
    )
