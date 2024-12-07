/**
 * @param s puzzle input in string format
 * @returns solution flag
 */
const run = (s: string): unknown => {
  // Your code goes here
  const [rawRules, inputs] = s.split("\n\n");
  if (!rawRules || !inputs) return 0;

  const potentialValues = new Set<number>();
  const rules: Array<[number, number]> = rawRules
    .trim()
    .split("\n")
    .map((rule) => {
      const min = parseInt(rule.substring(0, 2), 10);
      const max = parseInt(rule.substring(3, 5), 10);
      potentialValues.add(min).add(max);
      return [min, max];
    });

  const values = Array.from(potentialValues);
  const sortFollowingRules = (a: number, b: number) => {
    for (const rule of rules) {
      if (rule[0] === a && rule[1] === b) return -1;
      if (rule[0] === b && rule[1] === a) return 1;
    }
    return 0;
  };
  values.sort(sortFollowingRules);

  let sum = 0;
  for (const input of inputs.split("\n")) {
    if (!input) continue;

    const values = input.split(",").map((v) => parseInt(v, 10));
    const sortedValues = values.toSorted(sortFollowingRules);

    if (sortedValues.every((v, i) => v === values[i])) {
      continue;
    }

    const middleValue = sortedValues[Math.floor(values.length / 2)];
    sum += middleValue;
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
97,13,75,29,47`) === 123
);

if (Deno.args[0]) {
  const start = performance.now();
  const answer = run(Deno.args[0]);

  console.log(`_duration:${performance.now() - start}`);
  console.log(answer);
}
