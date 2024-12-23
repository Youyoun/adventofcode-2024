from tool.runners.python import SubmissionPy
import networkx as nx


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        G = nx.Graph()
        for line in s.split("\n"):
            a, b = line.split("-")
            G.add_edge(a, b)

        sets_of_3 = set()
        for node in G.nodes:
            for neighbor in G.neighbors(node):
                for neighbor2 in G.neighbors(neighbor):
                    if neighbor2 != node and G.has_edge(node, neighbor2):
                        sets_of_3.add(tuple(sorted([node, neighbor, neighbor2])))

        return sum(any(n.startswith("t") for n in set_of_3) for set_of_3 in sets_of_3)


def test_th_ch():
    """
    Run `python -m pytest ./day-23/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
""".strip()
        )
        == 7
    )
