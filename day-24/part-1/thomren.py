from collections import defaultdict
from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        init, gates = s.split("\n\n")
        values = {
            k: int(v) for k, v in (line.split(": ") for line in init.splitlines())
        }
        dependencies = {}
        used_in = defaultdict(list)
        for gate in gates.splitlines():
            in1, op, in2, _, out = gate.split()
            dependencies[out] = ((in1, in2), op)
            used_in[in1].append(out)
            used_in[in2].append(out)

        ready = [
            out
            for out, (inputs, _) in dependencies.items()
            if all(i in values for i in inputs)
        ]
        visited = set(values.keys()) | set(ready)
        while ready:
            wire = ready.pop()
            if wire in values:
                continue
            (in1, in2), op = dependencies[wire]
            values[wire] = OPS[op](values[in1], values[in2])
            for w in used_in.get(wire, []):
                if all(i in values for i in dependencies[w][0]) and not w in visited:
                    ready.append(w)
                    visited.add(w)

        z_wires = sorted([w for w in values if w.startswith("z")])
        return sum(values[w] * 2**i for i, w in enumerate(z_wires))


OPS = {
    "AND": lambda a, b: a & b,
    "OR": lambda a, b: a | b,
    "XOR": lambda a, b: a ^ b,
}


def test_thomren():
    """
    Run `python -m pytest ./day-24/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
""".strip()
        )
        == 4
    )

    assert (
        ThomrenSubmission().run(
            """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
""".strip()
        )
        == 2024
    )
