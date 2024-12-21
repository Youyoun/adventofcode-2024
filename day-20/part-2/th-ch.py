from tool.runners.python import SubmissionPy
from importlib import import_module

part1 = import_module("day-20.part-1.th-ch")


class ThChSubmission(SubmissionPy):
    def run(self, s: str, cheat_length=20, picoseconds_saved=100):
        """
        :param s: input in string format
        :return: solution flag
        """
        return part1.ThChSubmission().run(s, cheat_length, picoseconds_saved)


def test_th_ch():
    """
    Run `python -m pytest ./day-20/part-2/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
""".strip(), picoseconds_saved=50
        )
        == 285
    )
