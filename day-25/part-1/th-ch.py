from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        locks, keys = [], []
        for block in s.split("\n\n"):
            grid = [list(line) for line in block.splitlines()]
            structure = [
                sum(grid[y][x] == "#" for y in range(len(grid))) - 1
                for x in range(len(grid[0]))
            ]
            if all(grid[0][x] == "#" for x in range(len(grid[0]))):
                locks.append(structure)
            else:
                keys.append(structure)

        nb_fit = 0
        for lock in locks:
            for key in keys:
                if all(lock[x] + key[x] <= 5 for x in range(len(lock))):
                    nb_fit += 1

        return nb_fit


def test_th_ch():
    """
    Run `python -m pytest ./day-25/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
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
