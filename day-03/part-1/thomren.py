import re

from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        res = 0
        for m in re.findall(r"mul\((\d+),(\d+)\)", s):
            res += int(m[0]) * int(m[1])
        return res


def test_thomren():
    """
    Run `python -m pytest ./day-03/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
""".strip()
        )
        == 161
    )
