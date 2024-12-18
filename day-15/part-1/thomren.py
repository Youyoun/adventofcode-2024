from tool.runners.python import SubmissionPy

INSTRUCTIONS = {
    "<": (0, -1),
    ">": (0, 1),
    "^": (-1, 0),
    "v": (1, 0),
}


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        world, instructions = s.split("\n\n")
        bot_idx = world.index("@")
        world = [[c for c in line] for line in world.splitlines()]
        height, width = len(world), len(world[0])
        bot_pos = bot_idx // (width + 1), bot_idx % (width + 1)
        for ins in instructions.replace("\n", ""):
            dx, dy = INSTRUCTIONS[ins]
            x, y = bot_pos
            i, j = x + dx, y + dy
            while 0 <= i < height and 0 <= j < width and world[i][j] not in ["#", "."]:
                i += dx
                j += dy
            if not 0 <= i < height or not 0 <= j < width or world[i][j] == "#":
                continue
            bot_pos = x + dx, y + dy
            while i != x or j != y:
                world[i][j] = world[i - dx][j - dy]
                i -= dx
                j -= dy
            world[x][y] = "."
        res = 0
        for i in range(len(world)):
            for j in range(len(world[i])):
                if world[i][j] == "O":
                    res += 100 * i + j
        return res


def test_thomren():
    """
    Run `python -m pytest ./day-15/part-1/thomren.py` to test the submission.
    """
    assert (
        (
            ThomrenSubmission().run(
                """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
""".strip()
            )
        )
        == 2028
    )

    assert (
        ThomrenSubmission().run(
            """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""".strip()
        )
        == 10092
    )
