from tool.runners.python import SubmissionPy
from functools import cache


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        available_towels, designs = s.split("\n\n")
        towels = set(available_towels.split(", "))
        designs = designs.split("\n")

        @cache
        def is_design_possible(design):
            if not design:
                return True

            for towel in towels:
                if design.startswith(towel) and is_design_possible(design[len(towel) :]):
                    return True

            return False

        return sum(is_design_possible(design) for design in designs)


def test_th_ch():
    """
    Run `python -m pytest ./day-19/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
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
