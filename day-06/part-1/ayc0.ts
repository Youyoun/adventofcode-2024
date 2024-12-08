enum Direction {
  UP = 0,
  RIGHT = 1,
  DOWN = 2,
  LEFT = 3,
}

/**
 * @param s puzzle input in string format
 * @returns solution flag
 */
const run = (s: string): unknown => {
  const grid = s.replaceAll("\n", "");
  const nbLines = Math.sqrt(grid.length);

  const visited = new Set<number>();
  const addToVisited = (x: number, y: number) => visited.add(x * nbLines + y);

  const startPos = grid.indexOf("^");
  let x = Math.floor(startPos / nbLines);
  let y = startPos % nbLines;

  let direction: Direction = Direction.UP;

  addToVisited(x, y);

  while (x !== -1 && x !== nbLines && y !== -1 && y !== nbLines) {
    addToVisited(x, y);

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

    if (grid[nextX * nbLines + nextY] === "#") {
      direction = (direction + 1) % 4;
    } else {
      x = nextX;
      y = nextY;
    }
  }

  return visited.size;
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
......#...`) === 41
);

if (Deno.args[0]) {
  const start = performance.now();
  const answer = run(Deno.args[0]);

  console.log(`_duration:${performance.now() - start}`);
  console.log(answer);
}
