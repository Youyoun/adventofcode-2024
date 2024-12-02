from tool.runners.python import SubmissionPy


class Ayc0Submission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        safes = 0
        for line in s.splitlines():
            if not line:
                continue
            numbers = [int(n) for n in line.split()]
            is_going_up = numbers[0] < numbers[1]

            prev_number = numbers[0]
            safe = True
            for number in numbers[1:]:
                if is_going_up and prev_number >= number:
                    safe = False
                    break

                if not is_going_up and prev_number <= number:
                    safe = False
                    break

                distance = abs(prev_number - number)
                if distance > 3 or distance == 0:
                    safe = False
                    break

                prev_number = number

            if safe:
                safes += 1
        return safes

def test_ayc0():
    """
    Run `python -m pytest ./day-02/part-1/ayc0.py` to test the submission.
    """
    assert (
        Ayc0Submission().run(
            """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""".strip()
        )
        == 2
    )
