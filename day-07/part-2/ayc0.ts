function loop(
  result: number,
  acc: number,
  currentIndex: number,
  values: number[]
): boolean {
  if (values.length === currentIndex) {
    return acc === result;
  }

  if (acc > result) {
    return false;
  }

  const value = values[currentIndex];
  const nextIndex = currentIndex + 1;

  if (loop(result, acc * value, nextIndex, values)) {
    return true;
  }

  if (loop(result, acc + value, nextIndex, values)) {
    return true;
  }

  if (
    loop(result, acc * 10 ** String(value).length + value, nextIndex, values)
  ) {
    return true;
  }

  return false;
}

/**
 * @param s puzzle input in string format
 * @returns solution flag
 */
const run = (s: string): number => {
  let sum = 0;
  for (const line of s.trim().split("\n")) {
    if (!line) continue;
    const [result, ...values] = line.split(/:? /).map(Number);

    const res = loop(result, values[0], 1, values);
    if (res) {
      sum += result;
    }
  }

  return sum;
};

console.assert(
  run(`190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20`) === 11387
);

if (Deno.args[0]) {
  const start = performance.now();
  const answer = run(Deno.args[0]);

  console.log(`_duration:${performance.now() - start}`);
  console.log(answer);
}
