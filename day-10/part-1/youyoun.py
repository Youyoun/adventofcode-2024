from tool.runners.python import SubmissionPy


def trailhead_score(map_, i, j) -> set:
    height = map_[i][j]
    if height == 9:
        return {(i, j)}
    else:
        top_height_pos = set()
        if i > 0 and map_[i - 1][j] == height + 1:
            top_height_pos.update(trailhead_score(map_, i - 1, j))
        if i < len(map_) -1 and map_[i + 1][j] == height + 1:
            top_height_pos.update(trailhead_score(map_, i + 1, j))
        if j > 0 and map_[i][j - 1] == height + 1:
            top_height_pos.update(trailhead_score(map_, i, j - 1))
        if j < len(map_[i]) - 1 and map_[i][j + 1] == height + 1:
            top_height_pos.update(trailhead_score(map_, i, j + 1))
        return top_height_pos


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
                    total_score += len(trailhead_score(map_, i, j))
        return total_score


def test_example_1():
    """
    Run `python -m pytest ./day-10/part-1/youyoun.py` to test the submission.
    """
    assert (
        YouyounSubmission().run(
            """0123
1234
8765
9876""".strip()
        ) == 1
    )

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
        == 36
    )


def test_horizontal():
    """
    Run `python -m pytest ./day-10/part-1/youyoun.py` to test the submission.
    """
    assert (
        YouyounSubmission().run(
            """9876543210""".strip()
        )
        == 1
    )

def test_vertical():
    assert YouyounSubmission().run("""9
8
7
6
5
4
3
2
1
0""") == 1

def test_incomplete():
    assert YouyounSubmission().run("""98""") == 0

def test_two_trailheads():
    assert YouyounSubmission().run("""9876543210123456789""") == 2

def test_two_trailheads_complex():
    assert YouyounSubmission().run("""10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01""".replace(".", "0")) == 3

def test_youyoun_first_trailhead():
    """
    Run `python -m pytest ./day-10/part-1/youyoun.py` to test the submission.
    """
    assert (
        YouyounSubmission().run(
            """
89010...
78121...
.7.30...
.654....
45......
32......
01......
.0......""".replace(".", "9").strip()
        )
        == 6
    )

def test_example_2():
    assert YouyounSubmission().run("""..90..9
...1.98
...2..7
6543456
765.987
876....
987....""".replace(".", "8")) == 4