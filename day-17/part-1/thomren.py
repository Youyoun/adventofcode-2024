from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str, return_registers: bool = False):
        """
        :param s: input in string format
        :return: solution flag
        """
        registers = [0, 0, 0]
        lines = s.splitlines()
        registers[0] = int(lines[0].split(": ")[1])
        registers[1] = int(lines[1].split(": ")[1])
        registers[2] = int(lines[2].split(": ")[1])
        program = [int(x) for x in lines[-1].split(": ")[1].split(",")]

        computer = Computer(*registers, program)
        out = computer.run()
        if return_registers:
            return computer.registers
        return ",".join([str(o) for o in out])


class Computer:
    def __init__(self, A, B, C, program):
        self.registers = [A, B, C]
        self.program = program
        self.ip = 0

    def get_combo_operand(self, o):
        if o <= 3:
            return o
        if o <= 6:
            return self.registers[o - 4]
        raise ValueError(f"Invalid combo operand {o}")

    def run(self):
        outputs = []
        while self.ip >= 0 and self.ip < len(self.program):
            op = self.program[self.ip]
            match op:
                case 0:
                    self.registers[0] //= 2 ** self.get_combo_operand(
                        self.program[self.ip + 1]
                    )
                case 1:
                    self.registers[1] ^= self.program[self.ip + 1]
                case 2:
                    self.registers[1] = (
                        self.get_combo_operand(self.program[self.ip + 1]) % 8
                    )
                case 3:
                    if self.registers[0] != 0:
                        self.ip = self.program[self.ip + 1] - 2
                case 4:
                    self.registers[1] ^= self.registers[2]
                case 5:
                    outputs.append(
                        self.get_combo_operand(self.program[self.ip + 1]) % 8
                    )
                case 6:
                    self.registers[1] = self.registers[0] // (
                        2 ** self.get_combo_operand(self.program[self.ip + 1])
                    )
                case 7:
                    self.registers[2] = self.registers[0] // (
                        2 ** self.get_combo_operand(self.program[self.ip + 1])
                    )
                case _:
                    raise ValueError(f"Invalid opcode {op}")
            self.ip += 2
        return outputs


def test_thomren():
    """
    Run `python -m pytest ./day-17/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
Register A: 10
Register B: 0
Register C: 0

Program: 5,0,5,1,5,4
""".strip()
        )
        == "0,1,2"
    )

    assert (
        ThomrenSubmission().run(
            """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
""".strip()
        )
        == "4,2,5,6,7,7,7,7,3,1,0"
    )

    assert (
        ThomrenSubmission().run(
            """
Register A: 0
Register B: 2024
Register C: 43690

Program: 4,0
""".strip(),
            True,
        )
        == [0, 44354, 43690]
    )

    assert (
        ThomrenSubmission().run(
            """
Register A: 0
Register B: 29
Register C: 0

Program: 1,7
""".strip(),
            True,
        )
        == [0, 26, 0]
    )

    assert (
        ThomrenSubmission().run(
            """
Register A: 0
Register B: 0
Register C: 9

Program: 2,6
""".strip(),
            True,
        )
        == [0, 1, 9]
    )

    assert (
        ThomrenSubmission().run(
            """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
""".strip()
        )
        == "4,6,3,5,6,3,5,2,1,0"
    )
