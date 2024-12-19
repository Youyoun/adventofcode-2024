from functools import cache
from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        towels_str, designs_str = s.split("\n\n")
        towels = tuple(towels_str.split(", "))
        designs = designs_str.splitlines()
        return sum(num_combinations(towels, design) for design in designs)


@cache
def num_combinations(towels: tuple[str], design: str) -> bool:
    if len(design) == 0:
        return 1
    res = 0
    for towel in towels:
        if design.startswith(towel):
            res += num_combinations(towels, design[len(towel) :])
    return res


def test_thomren():
    """
    Run `python -m pytest ./day-19/part-2/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
""".strip()
        )
        == 16
    )
