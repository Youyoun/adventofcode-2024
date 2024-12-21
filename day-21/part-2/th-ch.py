from tool.runners.python import SubmissionPy
from importlib import import_module

part1 = import_module("day-21.part-1.th-ch")


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        return part1.ThChSubmission().run(s, nb_robots=25)


def test_th_ch():
    """
    Run `python -m pytest ./day-21/part-2/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
029A
980A
179A
456A
379A
""".strip()
        )
        == 154115708116294
    )
