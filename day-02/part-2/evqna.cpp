#include <chrono>
#include <iostream>
#include <span>
#include <sstream>
#include <string>
#include <vector>

bool safe_with_skip(const std::vector<int>& level, int k = -1) {
  bool inc = true, dec = true;
  int prev = -1;
  for (size_t i = 0; i < level.size(); i++) {
    if ((int)i == k) continue;
    if (prev >= 0) {
      int delta = level[i] - prev;
      if (abs(delta) < 1 || abs(delta) > 3) return false;
      inc = inc && delta >= 0;
      dec = dec && delta <= 0;
    }
    prev = level[i];
  }
  return inc || dec;
}

bool safe(const std::vector<int>& level) {
  if (safe_with_skip(level))  return true;
  for (size_t k = 0; k < level.size(); k++) {
    if (safe_with_skip(level, k)) return true;
  }
  return false;
}

int Run(const std::string& input) {
  std::istringstream iss(input);
  int safe_count = 0;
  for (std::string line; std::getline(iss, line);) {
    std::istringstream iss2(line);
    std::vector<int> level;
    int n;
    while (iss2 >> n) level.push_back(n);
    if (safe(level)) safe_count++;
  }
  return safe_count;
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
