#include <chrono>
#include <cstdint>
#include <functional>
#include <iostream>
#include <span>
#include <sstream>
#include <string>
#include <vector>

bool valid(int64_t result, const std::span<int> ops) {
  std::function<bool(int64_t, const std::span<int>)> rec;
  rec = [result, &rec](int64_t acc, const std::span<int> ops) -> bool {
    if (ops.empty()) return acc == result;
    return rec(acc + ops[0], ops.subspan(1)) || rec(acc * ops[0], ops.subspan(1));
  };
  return rec(0, ops);
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
