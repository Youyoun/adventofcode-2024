from collections import deque
from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str, n_bytes: int = 1024, size: int = 71) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        bytes_map = {
            tuple(map(int, line.split(","))) for line in s.splitlines()[:n_bytes]
        }
        queue = deque([(0, 0)])
        distances = {(0, 0): 0}
        while queue:
            pos = queue.popleft()
            if pos == (size - 1, size - 1):
                return distances[pos]
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_pos = (pos[0] + dx, pos[1] + dy)
                if (
                    new_pos not in bytes_map
                    and new_pos not in distances
                    and 0 <= new_pos[0] < size
                    and 0 <= new_pos[1] < size
                ):
                    distances[new_pos] = distances[pos] + 1
                    queue.append(new_pos)
        return -1


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
            n_bytes=12,
            size=7,
        )
        == 22
    )
