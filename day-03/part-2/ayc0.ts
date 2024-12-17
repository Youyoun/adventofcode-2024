const regex = /mul\((\d+),(\d+)\)|(don't\(\))|(do\(\))/g;

/**
 * @param s puzzle input in string format
 * @returns solution flag
 */
const run = (s: string): number => {
  // Your code goes here
  let sum = 0;
  let keep = true;
  for (const match of s.matchAll(regex)) {
    if (!match) {
      continue;
    }

    const [, a, b, dont, redo] = match;
    if (dont) {
      keep = false;
      continue;
    }
    if (redo) {
      keep = true;
      continue;
    }

    if (!keep) {
      continue;
    }
    sum += parseInt(a, 10) * parseInt(b, 10);
  }
  return sum;
};

console.assert(
  run(
    `xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))`
  ) === 48
);

const start = performance.now();
const answer = run(Deno.args[0] || "");

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
