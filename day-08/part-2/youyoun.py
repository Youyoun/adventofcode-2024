from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        pass


def test_youyoun():
    """
    Run `python -m pytest ./day-08/part-2/youyoun.py` to test the submission.
    """
    assert (
        YouyounSubmission().run(
            """
""".strip()
        )
        == None
    )
