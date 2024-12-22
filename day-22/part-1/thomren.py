from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        res = 0
        for line in s.splitlines():
            secret = int(line)
            for _ in range(2000):
                secret = next_secret(secret)
            res += secret
        return res


def next_secret(secret: int) -> int:
    x = secret * 64
    secret = (x ^ secret) % 16777216
    y = secret // 32
    secret = (y ^ secret) % 16777216
    z = secret * 2048
    secret = (z ^ secret) % 16777216
    return secret


def test_thomren():
    """
    Run `python -m pytest ./day-22/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
1
10
100
2024
""".strip()
        )
        == 37327623
    )
