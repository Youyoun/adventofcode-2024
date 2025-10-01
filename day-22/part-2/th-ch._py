from tool.runners.python import SubmissionPy
from functools import cache
from collections import defaultdict


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
            secret = prune(mix(secret, secret * 64))
            secret = prune(mix(secret, secret // 32))
            secret = prune(mix(secret, secret * 2048))
            return secret

        # { instruction : {initial_secret : bananas} }
        seqs = defaultdict(dict)

        for initial_secret in map(int, s.split("\n")):
            diffs = []
            secret = initial_secret
            for _ in range(2000):
                old_secret = secret
                secret = generate_next_secret(old_secret)
                diffs.append(secret % 10 - old_secret % 10)
                if len(diffs) >= 4:
                    diffs = diffs[-4:]
                    seq = tuple(diffs)
                    bananas = secret % 10
                    if initial_secret not in seqs[seq]:
                        seqs[seq][initial_secret] = bananas

        return max(sum(bananas.values()) for bananas in seqs.values())


def test_th_ch():
    """
    Run `python -m pytest ./day-22/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
1
2
3
2024
""".strip()
        )
        == 23
    )
