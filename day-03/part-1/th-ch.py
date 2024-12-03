from tool.runners.python import SubmissionPy

import re


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        muls = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", s)
        return sum(int(a) * int(b) for a, b in muls)


def test_th_ch():
    """
    Run `python -m pytest ./day-03/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
""".strip()
        )
        == 161
    )
