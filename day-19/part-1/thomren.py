from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        towels_str, designs_str = s.split("\n\n")
        towels = towels_str.split(", ")
        designs = designs_str.splitlines()
        return sum(is_possible(towels, design) for design in designs)


def is_possible(towels: list[str], design: str) -> bool:
    if len(design) == 0:
        return True
    for towel in towels:
        if design.startswith(towel) and is_possible(towels, design[len(towel) :]):
            return True
    return False


def test_thomren():
    """
    Run `python -m pytest ./day-19/part-1/thomren.py` to test the submission.
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
        == 6
    )
