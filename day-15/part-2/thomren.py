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

        # print("\n".join("".join(line) for line in world))
        # print()

        # scoring
        res = 0
        boxes = []
        for i in range(len(world)):
            for j in range(len(world[i])):
                if world[i][j] == "[":
                    boxes.append(f"{i},{j}")
                    res += 100 * i + j
        print("\n".join(boxes))
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
        if move(world, (x, y), (dx, dy)):
            bot_pos = x + dx, y + dy
            world[x + dx][y + dy] = "@"
            world[x][y] = "."
        if DEBUG:
            print(ins)
            print("\n".join("".join(line) for line in world))
            print()
    return world


def move_box(world, pos, direction):
    x, y = pos
    match direction:
        case (0, 1):
            if world[x][y + 2] == "[" and not move_box(world, (x, y + 2), direction):
                return False
            if world[x][y + 2] == "#":
                return False
            world[x][y + 1] = "["
            world[x][y + 2] = "]"
            world[x][y] = "."
        case (0, -1):
            if world[x][y - 1] == "]" and not move_box(world, (x, y - 2), direction):
                return False
            if world[x][y - 1] == "#":
                return False
            world[x][y - 1] = "["
            world[x][y] = "]"
            world[x][y + 1] = "."
        case (1, 0):
            if world[x + 1][y] == "#" or world[x + 1][y + 1] == "#":
                return False
            if world[x + 1][y] == "[" and not move_box(world, (x + 1, y), direction):
                return False
            if world[x + 1][y] == "]" and not move_box(
                world, (x + 1, y - 1), direction
            ):
                return False
            if world[x + 1][y + 1] == "[" and not move_box(
                world, (x + 1, y + 1), direction
            ):
                return False
            world[x + 1][y] = "["
            world[x + 1][y + 1] = "]"
            world[x][y] = "."
            world[x][y + 1] = "."
        case (-1, 0):
            if world[x - 1][y] == "#" or world[x - 1][y + 1] == "#":
                return False
            if world[x - 1][y] == "[" and not move_box(world, (x - 1, y), direction):
                return False
            if world[x - 1][y] == "]" and not move_box(
                world, (x - 1, y - 1), direction
            ):
                return False
            if world[x - 1][y + 1] == "[" and not move_box(
                world, (x - 1, y + 1), direction
            ):
                return False
            world[x - 1][y] = "["
            world[x - 1][y + 1] = "]"
            world[x][y] = "."
            world[x][y + 1] = "."
    return True


def move(world, pos, direction):
    x, y = pos
    dx, dy = direction
    if world[x + dx][y + dy] == "#":
        return False
    elif world[x + dx][y + dy] == ".":
        world[x + dx][y + dy] = world[x][y]
        world[x][y] = "."
        return True
    elif world[x + dx][y + dy] == "[":
        return move_box(world, (x + dx, y + dy), direction)
    elif world[x + dx][y + dy] == "]":
        return move_box(world, (x + dx, y + dy - 1), direction)


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
#..OOO#
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
##....[][]..##
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
