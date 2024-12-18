from collections import deque
from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str, size: int = 71) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        bytes_map = [tuple(map(int, line.split(","))) for line in s.splitlines()]
        blocks = set()
        path = set()
        for b in bytes_map:
            blocks.add(b)
            if b in path or not path:
                path = find_shortest_path(size, set(blocks))
            if not path:
                return f"{b[0]},{b[1]}"


def find_shortest_path(size: int, blocks: set[tuple[int, int]]) -> set[tuple[int, int]]:
    queue = deque([(0, 0)])
    previous = {(0, 0): None}
    while queue:
        pos = queue.popleft()
        if pos == (size - 1, size - 1):
            path = set()
            while pos is not None:
                path.add(pos)
                pos = previous[pos]
            return path
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            new_pos = (pos[0] + dx, pos[1] + dy)
            if (
                new_pos not in blocks
                and new_pos not in previous
                and 0 <= new_pos[0] < size
                and 0 <= new_pos[1] < size
            ):
                previous[new_pos] = pos
                queue.append(new_pos)
    return set()


def test_thomren():
    """
    Run `python -m pytest ./day-18/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
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
""".strip(),
            size=7,
        )
        == "6,1"
    )
