from collections import defaultdict
from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        g = defaultdict(set)
        for line in s.splitlines():
            a, b = line.split("-")
            g[a].add(b)
            g[b].add(a)

        cliques = []
        remaining = set(g.keys())
        while remaining:
            c = remaining.pop()
            clique = {c}
            stack = [n for n in g[c]]
            while stack:
                x = stack.pop()
                if not all(x in g[y] for y in clique):
                    continue
                clique.add(x)
                remaining.discard(x)
                for y in g[x]:
                    if y in remaining:
                        stack.append(y)
            cliques.append(clique)

        max_clique = max(cliques, key=len)
        return ",".join(sorted(max_clique))


def test_thomren():
    """
    Run `python -m pytest ./day-23/part-2/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
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
        == "co,de,ka,ta"
    )
