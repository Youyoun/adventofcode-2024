from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str, return_registers: bool = False):
        """
        2,4 -> B = A % 8
        1,1 -> B = B ^ 1
        7,5 -> C = A // 2**B
        0,3 -> A = A // 8
        1,4 -> B = B ^ 4
        4,4 -> B = B ^ (A // 2**(B^4))
        5,5 -> print(B % 8)
        3,0 -> if A != 0: goto 0

        out = (A % 8) ^ 1 ^ 4 ^ (A // 2 ** ((A % 8) ^ 1)) % 8
        """
        lines = s.splitlines()
        program = [int(x) for x in lines[-1].split(": ")[1].split(",")]

        solutions = {0}
        for out in program[::-1]:
            new_sol = set()
            for x in range(8):
                for sol in solutions:
                    y = (
                        x
                        ^ program[3]
                        ^ program[9]
                        ^ ((sol * 8 + x) // (2 ** (x ^ program[3])))
                    ) % 8
                    if y == out:
                        new_sol.add(sol * 8 + x)
            solutions = new_sol

        res = min(solutions)
        computer = Computer(res, 0, 0, program)
        out = computer.run()
        assert out == program

        return res


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
