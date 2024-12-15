#include <chrono>
#include <iostream>
#include <numeric>
#include <span>
#include <sstream>
#include <string>
#include <vector>

const int COST_A = 3, COST_B = 1;

struct Vec2 {
  int x, y;
  Vec2 operator+(const Vec2 o) const { return {x + o.x, y + o.y}; }
};

struct Machine {
  Vec2 bA, bB, prize;
};

std::vector<Machine> parse_input(const std::string& str) {
  auto parse_machine = [](const std::string& s) {
    const char* fmt =
        "Button A: X+%d, Y+%d Button B: X+%d, Y+%d Prize: X=%d, Y=%d";
    int ax, ay, bx, by, px, py;
    sscanf(s.c_str(), fmt, &ax, &ay, &bx, &by, &px, &py);
    return Machine{{ax, ay}, {bx, by}, {px, py}};
  };

  std::vector<Machine> machines;
  const std::string delim = "\n\n";
  std::size_t start = 0;
  std::size_t end = str.find(delim);
  while (end != std::string::npos) {
    machines.push_back(parse_machine(str.substr(start, end - start)));
    start = end + delim.length();
    end = str.find(delim, start);
  }
  machines.push_back(parse_machine(str.substr(start)));
  return machines;
}

// Solves `a*x + b*y = gcd(a,b)`
Vec2 extended_gcd(int a, int b) {
  bool flip = b > a;
  if (flip) std::swap(a, b);
  // https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
  int old_r = a, r = b;
  int old_s = 1, s = 0;
  int old_t = 0, t = 1;
  while (r != 0) {
    int q = old_r / r;
    int tmp = old_r - q*r;
    old_r = r; r = tmp;
    tmp = old_s - q*s;
    old_s = s; s = tmp;
    tmp = old_t - q*t;
    old_t = t; t = tmp;
  }
  if (flip) std::swap(old_s, old_t);
  return {old_s, old_t};
}

int nb_tokens(const Machine& m) {
  int c = std::gcd(m.bA.x, m.bB.x);
  int d = std::gcd(m.bA.y, m.bB.y);
  if (m.prize.x % c != 0 || m.prize.y % d != 0)
    return -1;

  int a1 = m.bA.x, b1 = m.bB.x;
  int u1 = a1 / c, v1 = b1 / c;
  int w1 = m.prize.x / c;
  Vec2 bezout1 = extended_gcd(a1, b1);
  int x1 = w1*bezout1.x, y1 = w1*bezout1.y;

  int a2 = m.bA.y, b2 = m.bB.y;
  int u2 = a2 / d, v2 = b2 / d;
  int w2 = m.prize.y / d;
  Vec2 bezout2 = extended_gcd(a2, b2);
  int x2 = w2*bezout2.x, y2 = w2*bezout2.y;

  // a1*(x1 - k1*v1) + b1*(y1 + k1*u1) = c
  // a2*(x2 - k2*v2) + b2*(y2 + k2*u2) = d

  // Solve for k1 and k2 in:
  // x1 - k1*v1 = x2 - k2*v2
  // y1 + k1*u1 = y2 + k2*u2
  int det = u1*v2 - u2*v1;
  if (det == 0) {
    // Input data seems to never contain this case.
    std::cout << "FAIL\n";
    return -1;
  }
  int k1 = (v2*(y2-y1) - u2*(x1-x2)) / det;
  int x = x1 - k1*v1;
  int y = y1 + k1*u1;

  // Chech integral solutions (k1/k2 may not be integers)
  if (a1*x + b1*y != m.prize.x || a2*x + b2*y != m.prize.y)
    return -1;
  if (x >= 0 && x <= 100 && y >= 0 && y <= 100)
    return x * COST_A + y * COST_B;
  return -1;
}

auto Run(const std::string& input) {
  int tokens = 0;
  for (const Machine& m : parse_input(input)) {
    int t = nb_tokens(m);
    if (t >= 0) tokens += t;
  }
  return tokens;
}

int main(int argc, char* argv[]) {
  if (argc < 2) {
    std::cout << "Missing one argument" << std::endl;
    exit(1);
  }
  auto args = std::span(argv, static_cast<size_t>(argc));

  auto start = std::chrono::high_resolution_clock::now();
  auto answer = Run(args[1]);
  auto end = std::chrono::high_resolution_clock::now();

  std::cout << "_duration:"
            << std::chrono::duration<float, std::milli>(end - start).count()
            << "\n";

  std::cout << answer << "\n";
  return 0;
}
