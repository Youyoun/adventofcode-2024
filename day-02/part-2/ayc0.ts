function isValid(numbers: number[]) {
  const isGoingUp = numbers[0] < numbers[1];
  let prevNumber = numbers[0];
  return numbers.every((n, i) => {
    if (i === 0) return true;

    try {
      if (isGoingUp && n < prevNumber) {
        return false;
      }
      if (!isGoingUp && n > prevNumber) {
        return false;
      }

      const diff = Math.abs(n - prevNumber);
      return 0 < diff && diff < 4;
    } finally {
      prevNumber = n;
    }
  });
}

/**
 * @param s puzzle input in string format
 * @returns solution flag
 */
const run = (s: string): unknown => {
  // Your code goes here

  let okays = 0;
  for (const line of s.split("\n")) {
    if (!line) continue;
    const numbers = line
      .trim()
      .split(" ")
      .map((n) => parseInt(n, 10));

    if (isValid(numbers)) {
      okays++;
      continue;
    }

    for (let i = 0; i < numbers.length; i++) {
      if (isValid(numbers.toSpliced(i, 1))) {
        okays++;
        break;
      }
    }
  }

  return okays;
};

console.assert(
  run(`7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9`) === 4
);

const start = performance.now();
const answer = run(Deno.args[0] || "");

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
