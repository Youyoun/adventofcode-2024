from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        locks, keys = [], []
        for schematic in s.split("\n\n"):
            lines = schematic.splitlines()
            counts = tuple(
                sum(lines[i][j] == "#" for i in range(len(lines))) - 1
                for j in range(len(lines[0]))
            )
            if all(x == "#" for x in lines[0]):
                locks.append(counts)
            else:
                keys.append(counts)

        return sum(
            all(k + l <= 5 for k, l in zip(key, lock)) for key in keys for lock in locks
        )


def test_thomren():
    """
    Run `python -m pytest ./day-25/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
""".strip()
        )
        == 3
    )
