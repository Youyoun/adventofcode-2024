from collections import defaultdict
from tool.runners.python import SubmissionPy

PATTERN_SIZE = 4


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        sequences = [get_sequence(int(line), 2000) for line in s.splitlines()]
        price_lists = [[x % 10 for x in seq] for seq in sequences]
        bananas_per_pattern = defaultdict(int)
        for prices in price_lists:
            monkey_patterns = set()
            diffs = tuple(prices[i] - prices[i - 1] for i in range(1, len(prices)))
            for i in range(len(diffs) - PATTERN_SIZE):
                pattern = diffs[i : i + PATTERN_SIZE]
                if pattern in monkey_patterns:
                    continue
                monkey_patterns.add(pattern)
                bananas_per_pattern[pattern] += prices[i + PATTERN_SIZE]
        return max(bananas_per_pattern.values())


def get_sequence(start: int, num: int) -> list[int]:
    sequence = [start]
    for _ in range(num):
        sequence.append(next_secret(sequence[-1]))
    return sequence


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
2
3
2024
""".strip()
        )
        == 23
    )
