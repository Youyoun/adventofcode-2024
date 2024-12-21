from tool.runners.python import SubmissionPy
from networkx import Graph, shortest_path_length
from networkx.exception import NetworkXNoPath


class ThChSubmission(SubmissionPy):
    def run(self, s: str, size=70, fallen_bytes=1024):
        """
        :param s: input in string format
        :return: solution flag
        """
        G = Graph()
        corrupted = set()
        lines = s.split("\n")
        for line in s.split("\n")[:fallen_bytes]:
            x, y = map(int, line.split(","))
            corrupted.add((x, y))

        for y in range(size+1):
            for x in range(size+1):
                if (x, y) in corrupted:
                    continue
                G.add_node((x, y))
                for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx <= size and 0 <= ny <= size and (nx, ny) not in corrupted:
                        G.add_edge((x, y), (nx, ny))

        while fallen_bytes < len(lines):
            fallen_bytes += 1
            x, y = map(int, lines[fallen_bytes].split(","))
            corrupted.add((x, y))
            G.remove_node((x, y))
            for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                nx, ny = x + dx, y + dy
                if G.has_edge((x, y), (nx, ny)):
                    G.remove_edge((x, y), (nx, ny))

            # print("\n".join("".join("#" if (x, y) in corrupted else "." for x in range(size+1)) for y in range(size+1)))

            try:
                shortest_path_length(G, source=(0, 0), target=(size, size))
            except NetworkXNoPath:
                return f"{x},{y}"



def test_th_ch():
    """
    Run `python -m pytest ./day-18/part-2/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
""".strip(), size=6, fallen_bytes=12
        )
        == "6,1"
    )
