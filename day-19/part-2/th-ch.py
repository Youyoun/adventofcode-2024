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
        def compute_nb_arrangements(design):
            if not design:
                return 1

            nb_arrangements = 0
            for towel in towels:
                if design.startswith(towel):
                    nb_arrangements += compute_nb_arrangements(design[len(towel) :])
            return nb_arrangements

        return sum(compute_nb_arrangements(design) for design in designs)


def test_th_ch():
    """
    Run `python -m pytest ./day-19/part-2/th-ch.py` to test the submission.
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
        == 16
    )
