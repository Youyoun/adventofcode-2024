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
    }
  }

  return okays;
};

const start = performance.now();
let input = "";
console.warn(Porffor.readArgv(1, input)); // useless to call in console.info, but there is a bug in the compiler
const answer = run(input);

console.log(`_duration:${String(performance.now() - start)}`);
console.log(answer);
