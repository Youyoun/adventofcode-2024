enum Direction {
  UP = 0,
  RIGHT = 1,
  DOWN = 2,
  LEFT = 3,
}

function testLoop(
  grid: string,
  nbLines: number,
  startPos: number,
  startDir: Direction,
  blocksToAdd: number,
  baseVisited: Set<number>
): number {
  let x = Math.floor(startPos / nbLines);
  let y = startPos % nbLines;

  let direction: Direction = startDir;

  // Duplicated content
  const visited = new Set<number>(baseVisited);

  let nbLoops = 0;

  while (x >= 0 && x < nbLines && y >= 0 && y < nbLines) {
    const currentIndex = x * nbLines + y;
    const key = currentIndex + direction * nbLines * nbLines;
    if (visited.has(key)) {
      return nbLoops + 1;
    }
    visited.add(key);

    let nextX = x;
    let nextY = y;

    switch (direction) {
      case Direction.UP:
        nextX = x - 1;
        break;
      case Direction.RIGHT:
        nextY = y + 1;
        break;
      case Direction.DOWN:
        nextX = x + 1;
        break;
      case Direction.LEFT:
        nextY = y - 1;
        break;
    }

    const rotatedDirection = (direction + 1) % 4;
    const nextIndex = nextX * nbLines + nextY;
    if (grid[nextIndex] === "#") {
      direction = rotatedDirection;
    } else {
      if (blocksToAdd) {
        const blockIndex = nextIndex;
        if (
          !visited.has(blockIndex) &&
          !visited.has(blockIndex + nbLines * nbLines) &&
          !visited.has(blockIndex + 2 * nbLines * nbLines) &&
          !visited.has(blockIndex + 3 * nbLines * nbLines)
        ) {
          nbLoops += testLoop(
            grid.substring(0, blockIndex) +
              "#" +
              grid.substring(blockIndex + 1),
            nbLines,
            currentIndex,
            rotatedDirection,
            blocksToAdd - 1,
            visited
          );
        }
      }

      x = nextX;
      y = nextY;
    }
  }

  return nbLoops;
}

/**
 * @param s puzzle input in string format
 * @returns solution flag
 */
const run = (s: string): unknown => {
  const grid = s.trim().replaceAll("\n", "");
  const nbLines = Math.sqrt(grid.length);

  const startPos = grid.indexOf("^");

  return testLoop(grid, nbLines, startPos, Direction.UP, 1, new Set());
};

console.assert(
  run(`....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...`) === 6
);

if (Deno.args[0]) {
  const start = performance.now();
  const answer = run(Deno.args[0]);

  console.log(`_duration:${performance.now() - start}`);
  console.log(answer);
}
