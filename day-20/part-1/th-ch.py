from tool.runners.python import SubmissionPy
from networkx import Graph, shortest_path_length
from collections import defaultdict
from pathos.multiprocessing import ProcessingPool as Pool
from functools import cache


class ThChSubmission(SubmissionPy):
    def run(self, s: str, cheat_length=2, picoseconds_saved=100):
        """
        :param s: input in string format
        :return: solution flag
        """
        G = Graph()
        grid = [list(line) for line in s.split("\n")]
        source, target = None, None

        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == "#":
                    continue
                if grid[y][x] == "S":
                    source = (x, y)
                elif grid[y][x] == "E":
                    target = (x, y)

                G.add_node((x, y))
                for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx <= len(grid[y]) and 0 <= ny <= len(grid) and grid[ny][nx] != "#":
                        G.add_edge((x, y), (nx, ny))

        @cache
        def path_length(source, target):
            return shortest_path_length(G, source=source, target=target)

        fastest = path_length(source=source, target=target)

        cheats = set()
        for start_x, start_y in G.nodes:
            for end_x, end_y in G.nodes:
                d = abs(end_x - start_x) + abs(end_y - start_y)
                if d <= cheat_length:
                    cheats.add((start_x, start_y, end_x, end_y))

        def try_cheat(cheat):
            start_x, start_y, end_x, end_y = cheat
            new_fastest1 = path_length(source=source, target=(start_x, start_y))
            d = abs(end_x - start_x) + abs(end_y - start_y)
            new_fastest2 = path_length(source=(end_x, end_y), target=target)
            return new_fastest1 + d + new_fastest2

        pool = Pool()
        results = pool.map(try_cheat, cheats) # can use tqdm_pathos to display a progress bar

        saved_times = defaultdict(int)
        for new_fastest in results:
            saved_times[fastest-new_fastest] += 1
        return sum(nb_cheats for saved_time, nb_cheats in saved_times.items() if saved_time >= picoseconds_saved)



def test_th_ch():
    """
    Run `python -m pytest ./day-20/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
""".strip(), picoseconds_saved=2
        )
        == 44
    )
