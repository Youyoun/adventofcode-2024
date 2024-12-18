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
    Run `python -m pytest ./day-17/part-2/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
""".strip()
        )
        == 117440
    )
