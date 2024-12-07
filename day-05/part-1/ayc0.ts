const createCheck = (min: string, max: string) => (input: string) => {
  const minIndex = input.indexOf(min);
  if (minIndex === -1) return true;
  const maxIndex = input.indexOf(max);
  if (maxIndex === -1) return true;
  return minIndex < maxIndex;
};

/**
 * @param s puzzle input in string format
 * @returns solution flag
 */
const run = (s: string): unknown => {
  // Your code goes here
  const [rules, inputs] = s.split("\n\n");
  if (!rules || !inputs) return 0;
  const checks: Array<(input: string) => boolean> = [];
  for (const rule of rules.split("\n")) {
    if (!rule) continue;
    const [min, max] = rule.split("|");
    checks.push(createCheck(min, max));
  }

  let sum = 0;
  for (const input of inputs.split("\n")) {
    if (!input) continue;
    if (!checks.every((check) => check(input))) {
      continue;
    }
    const values = input.split(",");
    const middleValue = values[Math.floor(values.length / 2)];
    sum += parseInt(middleValue, 10);
  }

  return sum;
};

console.assert(
  run(`47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47`) === 143
);

if (Deno.args[0]) {
  const start = performance.now();
  const answer = run(Deno.args[0]);

  console.log(`_duration:${performance.now() - start}`);
  console.log(answer);
}
