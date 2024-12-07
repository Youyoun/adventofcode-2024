#include <chrono>
#include <cstdint>
#include <functional>
#include <iostream>
#include <span>
#include <sstream>
#include <string>
#include <vector>

int64_t safe_stoll(const std::string& s) {
  if (s.empty())  return 0;
  return std::stoll(s);
}

bool valid(int64_t target, const std::span<int> ops) {
  std::function<bool(int64_t, const std::span<int>)> rec;
  // Processing operands right to left (top-down) lets us aggressively prune the search tree
  rec = [&rec](int64_t target, const std::span<int> ops) -> bool {
    int x = ops[ops.size() - 1];
    std::span<int> rest = ops.first(ops.size() - 1);

    if (rest.empty()) return target == x;

    if (x <= target && rec(target - x, rest))  return true;
    if (target % x == 0 && rec(target / x, rest))  return true;

    std::string s_t = std::to_string(target), s_x = std::to_string(x);
    return s_t.ends_with(s_x) && rec(safe_stoll(s_t.substr(0, s_t.size() - s_x.size())), rest);
  };
  if (ops.empty())  return target == 0;
  return rec(target, ops);
}

auto Run(const std::string& input) {
  std::istringstream iss(input);
  int64_t calibration = 0;
  for (std::string line; std::getline(iss, line);) {
    std::istringstream iss2(line);
    int64_t res;
    iss2 >> res;
    char c;
    iss2 >> c;  // ':'
    std::vector<int> operands;
    int n;
    while (iss2 >> n) operands.push_back(n);

    if (valid(res, operands)) calibration += res;
  }
  return calibration;
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
