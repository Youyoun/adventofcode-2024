import re

from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        res = 0
        mul_enabled = True
        for m in re.findall(r"(mul\((\d+),(\d+)\))|(do\(\))|(don't\(\))", s):
            if m[-1]:
                mul_enabled = False
            elif m[-2]:
                mul_enabled = True
            elif mul_enabled:
                res += int(m[1]) * int(m[2])
        return res


def test_thomren():
    """
    Run `python -m pytest ./day-03/part-2/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
""".strip()
        )
        == 48
    )
