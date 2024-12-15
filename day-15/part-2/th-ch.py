from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        grid, instructions = s.split("\n\n")
        if "[" not in grid:
            grid = (
                grid.replace("#", "##")
                .replace("O", "[]")
                .replace(".", "..")
                .replace("@", "@.")
            )

        obstacles = set()
        robot = None
        boxes = set()
        for y, line in enumerate(grid.split("\n")):
            for x, c in enumerate(line):
                if c == "#":
                    obstacles.add((x, y))
                elif c == "@":
                    robot = (x, y)
                elif c == "[":
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
            targets = set([(robot[0] + dx, robot[1] + dy)])
            should_apply = True
            while True:
                if any((x, y) in obstacles for x, y in targets):
                    should_apply = False
                    break

                new_targets = set()
                for x, y in targets:
                    if (x - 1, y) in boxes and (x - 1, y) not in boxes_to_move:
                        boxes_to_move.append((x - 1, y))
                        new_targets.update(
                            set([(x - 1 + dx, y + dy), (x + dx, y + dy)])
                        )
                    if (x, y) in boxes and (x, y) not in boxes_to_move:
                        boxes_to_move.append((x, y))
                        new_targets.update(
                            set([(x + dx, y + dy), (x + 1 + dx, y + dy)])
                        )

                if not new_targets:
                    break
                targets = new_targets

            if should_apply:
                boxes_to_move.reverse()
                for box in boxes_to_move:
                    boxes.remove(box)
                    boxes.add((box[0] + dx, box[1] + dy))
                robot = (robot[0] + dx, robot[1] + dy)

            # print_char = lambda p: (
            #     "#"
            #     if p in obstacles
            #     else (
            #         "["
            #         if p in boxes
            #         else (
            #             "]"
            #             if (p[0] - 1, p[1]) in boxes
            #             else ("@" if p == robot else ".")
            #         )
            #     )
            # )
            # print(
            #     "\n"
            #     + "\n".join(
            #         "".join(print_char((x, y)) for x in range(w)) for y in range(h)
            #     )
            # )
            # from time import sleep; sleep(0.1)

        return sum(100 * y + x for x, y in boxes)


def test_th_ch():
    """
    Run `python -m pytest ./day-15/part-2/th-ch.py` to test the submission.
    """

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
        == 9021
    )
