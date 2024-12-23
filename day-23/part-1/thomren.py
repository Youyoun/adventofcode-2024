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

        res = set()
        for c in g:
            if not c[0] == "t":
                continue
            for d in g[c]:
                for e in g[d]:
                    if e in g[c]:
                        res.add(frozenset((c, d, e)))
        return len(res)


def test_thomren():
    """
    Run `python -m pytest ./day-23/part-1/thomren.py` to test the submission.
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
        == 7
    )
