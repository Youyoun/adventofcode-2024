from tool.runners.python import SubmissionPy

INSTRUCTIONS = {
    "<": (0, -1),
    ">": (0, 1),
    "^": (-1, 0),
    "v": (1, 0),
}

EXPAND = {"#": "##", "O": "[]", ".": "..", "@": "@."}


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        world, instructions = s.split("\n\n")
        world = (
            world.replace("#", "##")
            .replace("O", "[]")
            .replace(".", "..")
            .replace("@", "@.")
        )
        bot_idx = world.index("@")
        world = [[c for c in line] for line in world.splitlines()]
        height, width = len(world), len(world[0])
        bot_pos = bot_idx // (width + 1), (bot_idx % (width + 1))
        print("\n".join("".join(line) for line in world))
        print()
        for ins in instructions.replace("\n", ""):
            dx, dy = INSTRUCTIONS[ins]
            x, y = bot_pos
            if move(world, (x, y), (dx, dy)):
                bot_pos = x + dx, y + dy
            print(ins)
            print("\n".join("".join(line) for line in world))
            print()
        res = 0
        for i in range(len(world)):
            for j in range(len(world[i])):
                if world[i][j] == "O":
                    res += 100 * i + j
        return res


def move(world, pos, direction):
    x, y = pos
    dx, dy = direction
    if world[x + dx][y + dy] == "#":
        return False
    if world[x + dx][y + dy] == ".":
        world[x + dx][y + dy] = world[x][y]
        world[x][y] = "."
        print(x, y, dx, dy)
        return True
    emptied = move(world, (x + dx, y + dy), direction)
    if not emptied:
        return False
    if world[x + dx][y + dy] == "[" and not move(
        world, (x + dx, y + 1 + dy), direction
    ):
        return False
    if world[x + dx][y + dy] == "]" and not move(
        world, (x + dx, y - 1 + dy), direction
    ):
        return False
    world[x + dx][y + dy] = world[x][y]
    world[x][y] = "."
    return True


def test_thomren():
    """
    Run `python -m pytest ./day-15/part-2/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
""".strip()
        )
        == 9021
    )
