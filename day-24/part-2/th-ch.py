from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        _, initial_cables = s.split("\n\n")
        highest_z = -1
        cables = {}
        for cable in initial_cables.split("\n"):
            operation, output = cable.split(" -> ")
            a, operator, b = operation.split(" ")
            cables[output] = (a, operator, b)
            if output.startswith("z"):
                highest_z = max(highest_z, int(output[1:]))

        # Circuit is a Ripple-Carry Adder, combining 1-bit full adders:
        # a --
        #     \
        #      XOR --- XOR ------- output
        # b --/  |   /
        # -------|--/
        #        |  \
        #         \-- AND -- OR -- …
        #   … ------- AND --/
        #   … -------/
        invalid = set()
        for output, (a, operator, b) in cables.items():
            # first and last bits are special cases and are valid in the input
            if "00" in [a[1:], b[1:], output[1:]] or str(highest_z) in [
                a[1:],
                b[1:],
                output[1:],
            ]:
                continue

            # If the output is a z but the operator is not XOR, it's invalid
            if output[0] == "z" and operator != "XOR":
                invalid.add(output)

            if operator == "XOR":
                # Either inputs are xN and yN, or output is zN
                if not (
                    (a[0] in ["x", "y"] and b[0] in ["x", "y"]) or output[0] == "z"
                ):
                    invalid.add(output)

                # In a 1-bit full adder, XOR can only feed XOR or AND
                for output2, (a2, operator2, b2) in cables.items():
                    if (output == a2 or output == b2) and operator2 == "OR":
                        invalid.add(output)

            # In a 1-bit full adder, AND can only feed OR
            if operator == "AND":
                for output2, (a2, operator2, b2) in cables.items():
                    if (output == a2 or output == b2) and operator2 != "OR":
                        invalid.add(output)

        return ",".join(sorted(invalid))
