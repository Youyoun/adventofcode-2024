import re
from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        regex = re.compile(r"(mul\((\d+),(\d+)\)|do\(\)|don't\(\))")
        sum = 0
        is_disabled = False
        for group in regex.findall(s):
            inst = group[0].split("(")[0]
            if "mul" == inst and not is_disabled:
                a, b = map(int, group[1:3])
                sum += a * b
            elif "do" == inst:
                is_disabled = False
            elif "don't" == inst:
                is_disabled = True
        return sum

def test_youyoun():
    """
    Run `python -m pytest ./day-03/part-1/youyoun.py` to test the submission.
    """
    assert (
            YouyounSubmission().run(
                """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))""".strip()
            )
            == 48
    )

