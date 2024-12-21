from collections import deque
from tool.runners.python import SubmissionPy

INSTRUCTIONS = {
    "<": (0, -1),
    ">": (0, 1),
    "^": (-1, 0),
    "v": (1, 0),
}

EXPAND = {"#": "##", "O": "[]", ".": "..", "@": "@."}

DEBUG = False


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        world, instructions = s.split("\n\n")
        world = simulate(world, instructions)

        # scoring
        res = 0
        boxes = []
        for i in range(len(world)):
            for j in range(len(world[i])):
                if world[i][j] == "[":
                    boxes.append(f"{i},{j}")
                    res += 100 * i + j
        return res


def simulate(world_str: str, instructions: str):
    # parsing
    world_str = (
        world_str.replace("#", "##")
        .replace("O", "[]")
        .replace(".", "..")
        .replace("@", "@.")
    )
    bot_idx = world_str.index("@")
    world = [[c for c in line] for line in world_str.splitlines()]
    height, width = len(world), len(world[0])
    bot_pos = bot_idx // (width + 1), (bot_idx % (width + 1))
    if DEBUG:
        print("Start state")
        print("\n".join("".join(line) for line in world))
        print()

    # simulation
    for ins in instructions.replace("\n", ""):
        dx, dy = INSTRUCTIONS[ins]
        x, y = bot_pos

        to_clear = deque([(x + dx, y + dy)])
        impossible = False
        boxes_to_move = []
        while to_clear:
            i, j = to_clear.popleft()
            if world[i][j] == "#" or not 0 <= i < height or not 0 <= j < width:
                impossible = True
                break
            if world[i][j] == "[":
                boxes_to_move.append((i, j))
                if dy == 0:
                    to_clear.extend([(i + dx, j), (i + dx, j + 1)])
                else:
                    to_clear.append((i, j + dy + 1))
            elif world[i][j] == "]":
                boxes_to_move.append((i, j - 1))
                if dy == 0:
                    to_clear.extend([(i + dx, j), (i + dx, j - 1)])
                else:
                    to_clear.append((i, j + dy - 1))

        if not impossible:
            for i, j in reversed(boxes_to_move):
                world[i][j] = "."
                world[i][j + 1] = "."
                world[i + dx][j + dy] = "["
                world[i + dx][j + dy + 1] = "]"
            bot_pos = x + dx, y + dy
            world[x + dx][y + dy] = "@"
            world[x][y] = "."

        if DEBUG:
            print(ins)
            print("\n".join("".join(line) for line in world))
            print()
    return world


def test_simulation():
    w = simulate(
        """
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######
""".strip(),
        "<",
    )
    assert (
        "\n".join("".join(line) for line in w)
        == """
##############
##......##..##
##..........##
##...[][]@..##
##....[]....##
##..........##
##############
""".strip()
    )

    w = simulate(
        """
#######
#.....#
#.OOOO#
#..OO@#
#..O..#
#.....#
#######
""".strip(),
        "<>vv<<<^",
    )
    assert (
        "\n".join("".join(line) for line in w)
        == """
##############
##..[][][]..##
##...[][].[]##
##....[]....##
##.....@....##
##..........##
##############
""".strip()
    )


def test_thomren():
    """
    Run `python -m pytest ./day-15/part-2/thomren.py` to test the submission.
    """
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
        == 9021
    )
