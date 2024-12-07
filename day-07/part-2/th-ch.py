from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        total = 0
        for equation in s.split("\n"):
            result, remaining = equation.split(":")
            result = int(result)
            numbers = list(map(int, remaining.split()))

            def reduce(numbers, target):
                if len(numbers) == 1:
                    return target == numbers[0]

                # add
                if target - numbers[-1] >= 0:
                    if reduce(numbers[:-1], target - numbers[-1]):
                        return True
                # multiply
                if target % numbers[-1] == 0:
                    if reduce(numbers[:-1], target // numbers[-1]):
                        return True
                # concatenation
                str_target = str(target)
                str_number = str(numbers[-1])
                if len(str_target) > len(str_number) and str_target.endswith(
                    str_number
                ):
                    if reduce(numbers[:-1], int(str_target[: -len(str_number)])):
                        return True

                return False

            if reduce(numbers, result):
                total += result

        return total


def test_th_ch():
    """
    Run `python -m pytest ./day-07/part-2/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".strip()
        )
        == 11387
    )
