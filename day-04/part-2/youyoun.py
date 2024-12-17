from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        lines = s.split("\n")
        n = len(lines)
        count = 0
        for i in range(1, n-1):
            for j in range(1, n-1):
                if lines[i][j] == "A":
                    if lines[i-1][j-1] == "M":
                        if lines[i-1][j+1] == "M":
                            count+=int(lines[i+1][j-1] == "S" and lines[i+1][j+1] == "S")
                        elif lines[i-1][j+1] == "S":
                            count += int(lines[i+1][j-1] == "M" and lines[i+1][j+1] == "S")
                    elif lines[i-1][j-1] == "S":
                        if lines[i-1][j+1] == "M":
                            count += int(lines[i+1][j-1] == "S" and lines[i+1][j+1] == "M")
                        elif lines[i-1][j+1] == "S":
                            count += int(lines[i+1][j-1] == "M" and lines[i+1][j+1] == "M")
        return count


def test_youyoun():
    """
    Run `python -m pytest ./day-04/part-2/youyoun.py` to test the submission.
    """
    assert (
        YouyounSubmission().run(
            """.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........""".strip()
        )
        == 9
    )
