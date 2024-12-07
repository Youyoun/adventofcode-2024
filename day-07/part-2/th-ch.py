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
            def reduce(numbers, target, acc):
                if not numbers:
                    return [acc == target]
                outcomes = []
                for potential_acc in [acc + numbers[0], acc * numbers[0], int(f"{acc}{numbers[0]}")]:
                    if potential_acc > target:
                        outcomes.append(False)
                        continue
                    outcomes.extend(reduce(numbers[1:], target, potential_acc))
                return outcomes

            if any(reduce(numbers[1:], result, numbers[0])):
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
