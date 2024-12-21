from tool.runners.python import SubmissionPy
import networkx as nx
from functools import cache

# Numeric keypad
G = nx.Graph()
G.add_node("A")
for n in range(10):
    G.add_node(str(n))
for a, b in [
    (7, 4),
    (7, 8),
    (8, 5),
    (8, 9),
    (9, 6),
    (4, 5),
    (4, 1),
    (5, 2),
    (5, 6),
    (6, 3),
    (1, 2),
    (2, 3),
    (2, 0),
    (3, "A"),
    (0, "A"),
]:
    G.add_edge(str(a), str(b))


def numeric_to_instruction(a, b):
    if a == "A":
        return "<" if b == "0" else "^"
    if b == "A":
        return "v" if a == "3" else ">"
    a, b = int(a), int(b)
    if a - b == 1:
        return "<"
    if a - b == -1:
        return ">"
    if a - b == 3:
        return "v"
    if a - b == -3:
        return "^"
    if a - b == 2:
        return "v"
    if a - b == -2:
        return "^"


def numeric_path_to_instruction(path):
    return "".join(
        numeric_to_instruction(path[i], path[i + 1]) for i in range(len(path) - 1)
    )


# Directional keypad
G2 = nx.Graph()
for n in ["A", "v", "<", ">", "^"]:
    G2.add_node(n)
for edge in [("^", "A"), ("^", "v"), ("A", ">"), ("v", ">"), ("v", "<")]:
    G2.add_edge(*edge)


def instruction_to_instruction(a, b):
    # A
    if a == "A":
        return "<" if b == "^" else "v"
    if b == "A":
        return ">" if a == "^" else "^"
    # ^
    if a == "^" and b == "v":
        return "v"
    if a == "v" and b == "^":
        return "^"
    # <
    if a == "<":
        return ">"
    if b == "<":
        return "<"
    # >
    if a == ">":
        return "<"
    if b == ">":
        return ">"


def instruction_path_to_instruction(path):
    return "".join(
        instruction_to_instruction(path[i], path[i + 1]) for i in range(len(path) - 1)
    )


# Get the length of a sequence of instructions
@cache
def get_seq_length(seq, depth):
    if depth == 0:
        return len(seq)
    new_seq = "A" + seq
    length = 0
    for i in range(len(new_seq) - 1):
        length += get_nb_moves(new_seq[i], new_seq[i + 1], depth)
    return length


@cache
def get_nb_moves(source, target, depth):
    length = float("inf")
    for path in nx.all_shortest_paths(G2, source=source, target=target):
        seq = instruction_path_to_instruction(path) + "A"
        length = min(length, get_seq_length(seq, depth - 1))
    return length


class ThChSubmission(SubmissionPy):
    def run(self, s: str, nb_robots=2):
        """
        :param s: input in string format
        :return: solution flag
        """
        complexities = 0
        for instruction in s.split("\n"):
            c = "A" + instruction
            seqs = []
            for i in range(len(c) - 1):
                paths = nx.all_shortest_paths(G, source=c[i], target=c[i + 1])
                seqs = [
                    seq + numeric_path_to_instruction(path) + "A"
                    for path in paths
                    for seq in seqs or [""]
                ]

            ################

            complexity = min(get_seq_length(seq, nb_robots) for seq in seqs) * int(
                instruction.replace("A", "")
            )
            complexities += complexity

        return complexities


def test_th_ch():
    """
    Run `python -m pytest ./day-21/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
029A
980A
179A
456A
379A
""".strip()
        )
        == 126384
    )
