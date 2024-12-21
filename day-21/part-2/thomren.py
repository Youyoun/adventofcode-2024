from collections import deque
from functools import cache
from tool.runners.python import SubmissionPy

DIR_PAD = {"A": (0, 2), "^": (0, 1), "v": (1, 1), "<": (1, 0), ">": (1, 2)}

NUM_PAD = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        return sum(
            get_shortest_seq_len(code, 26, "num") * int(code[:-1])
            for code in s.splitlines()
        )


@cache
def get_paths(start: tuple[int, int], end: tuple[int, int], pad_mode: str) -> list[str]:
    q = deque([(start, "")])
    paths = []
    while q:
        pos, path = q.popleft()
        if pos == end:
            paths.append(path + "A")
            continue
        if end[0] > pos[0] and not (pad_mode == "num" and pos[0] == 2 and pos[1] == 0):
            q.append(((pos[0] + 1, pos[1]), path + "v"))
        if end[0] < pos[0] and not (pad_mode == "dir" and pos[0] == 1 and pos[1] == 0):
            q.append(((pos[0] - 1, pos[1]), path + "^"))
        if end[1] > pos[1]:
            q.append(((pos[0], pos[1] + 1), path + ">"))
        if (
            end[1] < pos[1]
            and not (pad_mode == "num" and pos[0] == 3 and pos[1] == 1)
            and not (pad_mode == "dir" and pos[0] == 0 and pos[1] == 1)
        ):
            q.append(((pos[0], pos[1] - 1), path + "<"))
    return paths


@cache
def get_shortest_seq_len(code: str, num_bots: int, pad_mode: str = "num") -> int:
    if num_bots == 0:
        return len(code)

    pad = NUM_PAD if pad_mode == "num" else DIR_PAD
    pos = pad["A"]
    res = 0
    for d in code:
        target = pad[d]
        res += min(
            get_shortest_seq_len(path, num_bots - 1, "dir")
            for path in get_paths(pos, target, pad_mode)
        )
        pos = target
    return res
