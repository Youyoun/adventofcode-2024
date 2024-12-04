from tool.runners.python import SubmissionPy
import re

class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        regex = re.compile(r"mul\((\d+),(\d+)\)")
        sum = 0
        for group in regex.findall(s):
            a, b = map(int, group)
            sum += a * b
        return sum

def test_youyoun():
    """
    Run `python -m pytest ./day-03/part-1/youyoun.py` to test the submission.
    """
    assert (
        YouyounSubmission().run(
            """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))""".strip()
        )
        == 161
    )
