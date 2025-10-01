from tool.runners.python import SubmissionPy
from functools import cache


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        mix = lambda value, secret: value ^ secret
        prune = lambda secret: secret % 16777216

        @cache
        def generate_next_secret(secret):
            for _ in range(2000):
                secret = prune(mix(secret, secret * 64))
                secret = prune(mix(secret, secret // 32))
                secret = prune(mix(secret, secret * 2048))
            return secret

        return sum(generate_next_secret(secret) for secret in map(int, s.split("\n")))


def test_th_ch():
    """
    Run `python -m pytest ./day-22/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
1
10
100
2024
""".strip()
        )
        == 37327623
    )
