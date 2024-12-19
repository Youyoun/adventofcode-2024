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
        ip = 0

        def get_combo_operand(o):
            if o <= 3:
                return o
            if o <= 6:
                return registers[o - 4]
            raise ValueError(f"Invalid combo operand {o}")

        outputs = []
        while ip >= 0 and ip < len(program):
            op = program[ip]
            match op:
                case 0:
                    registers[0] //= 2 ** get_combo_operand(program[ip + 1])
                case 1:
                    registers[1] ^= program[ip + 1]
                case 2:
                    registers[1] = get_combo_operand(program[ip + 1]) % 8
                case 3:
                    if registers[0] != 0:
                        ip = program[ip + 1] - 2
                case 4:
                    registers[1] ^= registers[2]
                case 5:
                    outputs.append(get_combo_operand(program[ip + 1]) % 8)
                case 6:
                    registers[1] = registers[0] // (
                        2 ** get_combo_operand(program[ip + 1])
                    )
                case 7:
                    registers[2] = registers[0] // (
                        2 ** get_combo_operand(program[ip + 1])
                    )
                case _:
                    raise ValueError(f"Invalid opcode {op}")
            ip += 2

        if return_registers:
            return registers
        return ",".join([str(o) for o in outputs])


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
