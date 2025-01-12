/**
 * @param {string} s puzzle input in string format
 * @returns {unknown} solution flag
 */
const run = (s) => {
  // Your code goes here
};

console.assert(run(`example`) === "solution");

if (Deno.args[0]) {
  const start = performance.now();
  const answer = run(Deno.args[0]);

  console.log(`_duration:${performance.now() - start}`);
  console.log(answer);
}
