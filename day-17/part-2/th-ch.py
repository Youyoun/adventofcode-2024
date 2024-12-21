from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        lines = s.split("\n")
        program = list(map(int, lines[4].replace("Program: ", "").split(",")))
        b, c = int(lines[1].split(":")[1]), int(lines[2].split(":")[1])

        def solve(registers):
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

            pointer = 0
            output = []

            while pointer<len(program)-1:
                has_pointer_been_updated=False
                instruction, operand = program[pointer], program[pointer+1]
                if instruction == 0:
                    registers['A'] = registers['A']//2**combo( operand)
                elif instruction == 1:
                    registers['B'] = registers['B'] ^ literal(operand)
                elif instruction == 2:
                    registers['B'] = combo( operand) % 8
                elif instruction == 3:
                    if registers['A'] != 0:
                        pointer = literal(operand)
                        has_pointer_been_updated = True
                elif instruction == 4:
                    registers['B'] =registers['B'] ^ registers['C']
                elif instruction == 5:
                    output.append(combo(operand) % 8)
                elif instruction == 6:
                    registers['B'] = registers['A']//2**combo(operand)
                elif instruction == 7:
                    registers['C'] = registers['A']//2**combo(operand)

                if not has_pointer_been_updated:
                    pointer += 2

            return output


        # The program runs as a loop, each time:
        #    - dividing A by 8 ("0,3" instruction)
        #    - generating one output which is the last 3 bits of A
        # So we can generate the output in reverse order:
        #    - trying all 3 bits values (0 to 7) to find the correct output
        #    - then multiply A by 8
        def find_a_to_match_program(a, cursor):
            for n in range(8):
                next_a = 8*a+n
                output = solve({'A': next_a, 'B': b, 'C': c})
                if output == program[cursor:]:
                    if cursor == 0:
                        return next_a

                    next_a = find_a_to_match_program(next_a, cursor-1)
                    if next_a is not None:
                        return next_a

        a = 0 # The program ends with a "3,0" instruction so final value of A must be 0
        a = find_a_to_match_program(a, cursor=len(program)-1)
        # print(solve({'A': a, 'B': b, 'C': c})) # Checking the output is the program

        return a


def test_th_ch():
    """
    Run `python -m pytest ./day-17/part-2/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
""".strip()
        )
        == 117440
    )
