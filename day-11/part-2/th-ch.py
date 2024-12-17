from tool.runners.python import SubmissionPy
from importlib import import_module

part1 = import_module("day-11.part-1.th-ch")


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        return part1.ThChSubmission().run(s, nb_steps=75)


def test_th_ch():
    """
    Run `python -m pytest ./day-11/part-2/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
125 17
""".strip()
        )
        == 65601038650482
    )
