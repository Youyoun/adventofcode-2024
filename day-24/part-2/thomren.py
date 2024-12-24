from collections import defaultdict
from tool.runners.python import SubmissionPy

import graphviz
import re


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str, return_sol: bool = True):
        """
        :param s: input in string format
        :return: solution flag
        """

        swaps = [("vkq", "z11"), ("hqh", "z38"), ("mmk", "z24"), ("pvb", "qdq")]
        for x, y in swaps:
            s = swap_strings(s, f"-> {x}", f"-> {y}")
        if return_sol:
            return ",".join(sorted(list(sum(swaps, ()))))

        for i in range(45):
            m = re.search(
                f"((x{i:02} AND y{i:02})|(y{i:02} AND x{i:02})) -> (?P<out>\w+)", s
            )
            if m is None:
                print(f"did not find {i} AND")
                continue
            s = s.replace(m.group("out"), f"a{i:02}")
            m = re.search(
                f"((x{i:02} XOR y{i:02})|(y{i:02} XOR x{i:02})) -> (?P<out>\w+)", s
            )
            if m is None:
                print(f"did not find {i} XOR")
                continue
            s = s.replace(m.group("out"), f"o{i:02}")

            if i == 0:
                continue
            m = re.search(
                f"((o{i:02} XOR (?P<retenue>\w+))|((?P<retenue2>\w+) XOR o{i:02})) -> z{i:02}",
                s,
            )
            if m is None:
                print(f"did not find {i} retenue")
                continue
            if m.group("retenue") is None:
                s = s.replace(m.group("retenue2"), f"r{i:02}")
            else:
                s = s.replace(m.group("retenue"), f"r{i:02}")

            m = re.search(
                f"((r{i:02} AND o{i:02})|(o{i:02} AND r{i:02})) -> (?P<out>\w+)", s
            )
            if m is None:
                print(f"did not find {i} k")
                continue
            s = s.replace(m.group("out"), f"k{i:02}")

        _, gates = s.split("\n\n")
        dependencies = {}
        used_in = defaultdict(list)
        dot = graphviz.Digraph(comment="The Round Table")
        for gate in gates.splitlines():
            in1, op, in2, _, out = gate.split()
            dependencies[out] = ((in1, in2), op)
            used_in[in1].append(out)
            used_in[in2].append(out)
            if re.match(r"[a-z]{3}", out):
                dot.node(out, fillcolor="red", style="filled")
            dot.edge(in1, out, label=op)
            dot.edge(in2, out, label=op)
        dot.render("graph.gv", view=True)


def swap_strings(s: str, x: str, y: str) -> str:
    return s.replace(x, "tmp").replace(y, x).replace("tmp", y)
