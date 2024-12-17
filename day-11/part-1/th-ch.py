from tool.runners.python import SubmissionPy
import functools


@functools.cache
def blink(stone, nb_steps):
    if nb_steps == 0:
        return 1

    if stone == 0:
        return blink(1, nb_steps - 1)

    str_stone = str(stone)
    if len(str_stone) % 2 == 0:
        return blink(int(str_stone[: len(str_stone) // 2]), nb_steps - 1) + blink(
            int(str_stone[len(str_stone) // 2 :]), nb_steps - 1
        )

    return blink(stone * 2024, nb_steps - 1)


class ThChSubmission(SubmissionPy):
    def run(self, s: str, nb_steps=25):
        """
        :param s: input in string format
        :return: solution flag
        """
        stones = list(map(int, s.split()))
        return sum(blink(stone, nb_steps) for stone in stones)


def test_th_ch():
    """
    Run `python -m pytest ./day-11/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
125 17
""".strip()
        )
        == 55312
    )
