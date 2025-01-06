from tool.runners.python import SubmissionPy


def trailhead_rating(map_, i, j) -> int:
    height = map_[i][j]
    if height == 9:
        return 1
    else:
        rating = 0
        if i > 0 and map_[i - 1][j] == height + 1:
            rating += trailhead_rating(map_, i - 1, j)
        if i < len(map_) -1 and map_[i + 1][j] == height + 1:
            rating += trailhead_rating(map_, i + 1, j)
        if j > 0 and map_[i][j - 1] == height + 1:
            rating += trailhead_rating(map_, i, j - 1)
        if j < len(map_[i]) - 1 and map_[i][j + 1] == height + 1:
            rating += trailhead_rating(map_, i, j + 1)
        return rating


class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        map_ = [list(map(int, list(line))) for line in s.splitlines()]
        total_score = 0
        for i in range(len(map_)):
            for j in range(len(map_[0])):
                if map_[i][j] == 0:
                    total_score += trailhead_rating(map_, i, j)
        return total_score


def test_youyoun():
    """
    Run `python -m pytest ./day-10/part-1/youyoun.py` to test the submission.
    """
    assert (
        YouyounSubmission().run(
            """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""".strip()
        )
        == 81
    )