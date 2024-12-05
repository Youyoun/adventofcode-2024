const regex = /mul\((\d+),(\d+)\)/g;

/**
 * @param s puzzle input in string format
 * @returns solution flag
 */
const run = (s: string): number => {
  // Your code goes here
  let sum = 0;
  for (const match of s.matchAll(regex)) {
    if (!match) {
      continue;
    }

    const [, a, b] = match;
    sum += parseInt(a, 10) * parseInt(b, 10);
  }
  return sum;
};

console.assert(
  run(
    `xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))`
  ) === 161
);

const start = performance.now();
const answer = run(Deno.args[0] || "");

console.log(`_duration:${performance.now() - start}`);
console.log(answer);