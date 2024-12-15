from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        grid, instructions = s.split("\n\n")
        obstacles = set()
        robot = None
        boxes = set()
        for y, line in enumerate(grid.split("\n")):
            for x, c in enumerate(line):
                if c == "#":
                    obstacles.add((x, y))
                elif c == "@":
                    robot = (x, y)
                elif c == "O":
                    boxes.add((x, y))
        w, h = x + 1, y + 1

        for move in instructions.replace("\n", ""):
            if move == "^":
                dx, dy = 0, -1
            elif move == ">":
                dx, dy = 1, 0
            elif move == "<":
                dx, dy = -1, 0
            elif move == "v":
                dx, dy = 0, 1
            else:
                raise Exception("invalid", move)

            boxes_to_move = []
            target = (robot[0] + dx, robot[1] + dy)
            while target in boxes:
                boxes_to_move.append(target)
                target = (target[0] + dx, target[1] + dy)
            if target not in obstacles:
                if boxes_to_move:
                    boxes.remove(boxes_to_move[0])
                    boxes.add(target)
                robot = (robot[0] + dx, robot[1] + dy)

            # print_char = lambda p: (
            #     "#"
            #     if p in obstacles
            #     else ("O" if p in boxes else ("@" if p == robot else "."))
            # )
            # print(
            #     "\n"
            #     + "\n".join(
            #         "".join(print_char((x, y)) for x in range(w)) for y in range(h)
            #     )
            # )

        return sum(100 * y + x for x, y in boxes)


def test_th_ch():
    """
    Run `python -m pytest ./day-15/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
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
        == 2028
    )

    assert (
        ThChSubmission().run(
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
