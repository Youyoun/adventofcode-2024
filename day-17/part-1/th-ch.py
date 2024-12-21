from tool.runners.python import SubmissionPy
from operator import xor


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        lines = s.split("\n")
        registers = {'A': int(lines[0].split(":")[1]), 'B':  int(lines[1].split(":")[1]), 'C':  int(lines[2].split(":")[1])}
        program = list(map(int, lines[4].replace("Program: ", "").split(",")))
        pointer = 0

        def combo(operand):
            if operand<=3:
                return operand
            elif operand == 4:
                return registers['A']
            elif operand == 5:
                return registers['B']
            elif operand == 6:
                return registers['C']
            else:
                raise Exception("Invalid operand")
        literal = lambda operand: operand
        output = []

        while pointer < len(program)-1:
            has_pointer_been_updated = False
            instruction, operand = program[pointer], program[pointer+1]
            if instruction == 0:
                registers['A'] = registers['A']//2**combo(operand)
            elif instruction == 1:
                registers['B'] = xor(registers['B'], literal(operand))
            elif instruction == 2:
                registers['B'] = combo(operand)%8
            elif instruction == 3:
                if registers['A'] != 0:
                    pointer = literal(operand)
                    has_pointer_been_updated = True
            elif instruction == 4:
                registers['B'] = xor(registers['B'], registers['C'])
            elif instruction == 5:
                output.append(combo(operand) % 8)
            elif instruction == 6:
                registers['B'] = registers['A']//2**combo(operand)
            elif instruction == 7:
                registers['C'] = registers['A']//2**combo(operand)

            if not has_pointer_been_updated:
                pointer += 2

        return ",".join(map(str, output))


def test_th_ch():
    """
    Run `python -m pytest ./day-17/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
""".strip()
        )
        == "4,6,3,5,6,3,5,2,1,0"
    )
