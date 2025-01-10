import functools

from tool.runners.python import SubmissionPy

def sub_coords(coord_A, coord_B):
    return (coord_A[0] - coord_B[0], coord_A[1] - coord_B[1])

def is_valid_position(position):
    return position[0] > 0 and position[1] > 0

def parse_input(s):
    claw_machines = []
    for machine_lines in s.split("\n\n"):
        machine_dict = {"buttons": [], "prize": None}
        for line in machine_lines.splitlines():
            if line.startswith("Button"):
                x, y = [int(i.strip()) for i in line.split(":")[1].replace("X+","").replace("Y+","").split(",")]
                machine_dict["buttons"].append((x, y))
            elif line.startswith("Prize"):
                prize_x, prize_y = [int(i.strip()) for i in line.split(":")[1].replace("X=","").replace("Y=","").split(",")]
                machine_dict["prize"] = (prize_x + 10000000000000, prize_y + 10000000000000)
        claw_machines.append(machine_dict)
    return claw_machines

def solve(prize, buttons):
    """
    Simple linear problem, we can solve it explicitly.
    Seems that all problems either have a single solution or no solution at all,
    so we dont handle the case where there are multiple solutions (P colinear with M)
    """
    a1, a2 = buttons[0]
    b1, b2 = buttons[1]
    p1, p2 = prize
    det = a1 * b2 - a2 * b1
    if det != 0:
        a = (b2 * p1 - b1 * p2) / det
        b = (-a2 * p1 + a1 * p2) / det
        return a, b

def is_natural(a):
    return a == int(a) and a >= 0

class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        machines = parse_input(s)
        cost = 0
        for machine in machines:
            button_A = machine["buttons"][0]
            button_B = machine["buttons"][1]
            prize_location = machine["prize"]
            solution = solve(prize_location, (button_A, button_B))
            if solution is None:
                continue
            if is_natural(solution[0]) and is_natural(solution[1]):
                cost += 3 * solution[0] + solution[1]
        return int(cost)


def test_youyoun():
    """
    Run `python -m pytest ./day-13/part-2/youyoun.py` to test the submission.
    """
    assert (
        YouyounSubmission().run(
            """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=10000000008400, Y=10000000005400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=10000000007870, Y=10000000006450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=10000000018641, Y=10000000010279""".strip()
        )
        == 875318608908
    )
