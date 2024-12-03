from tool.runners.python import SubmissionPy

import re

class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        mul_regex = r"mul\((\d{1,3}),(\d{1,3})\)"
        do_regex = r"(do\(\)|don't\(\))"
        i = 0
        is_do = True
        total = 0
        while i < len(s):
            mul_match = re.search(mul_regex, s[i:])
            do_match = re.search(do_regex, s[i:])
            mul_start = mul_match.start() if mul_match else None
            do_start = do_match.start() if do_match else None

            if mul_start is None and do_start is None:
                break

            if mul_start is not None and (do_start is None or mul_start < do_start):
                if is_do:
                    total += int(mul_match.group(1)) * int(mul_match.group(2))
                i += mul_match.end()
            elif do_start is not None and (mul_start is None or do_start < mul_start):
                is_do = do_match.group() == "do()"
                i += do_match.end()

        return total


def test_th_ch():
    """
    Run `python -m pytest ./day-03/part-2/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
""".strip()
        )
        == 48
    )
