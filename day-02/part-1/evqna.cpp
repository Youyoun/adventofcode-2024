#include <chrono>
#include <iostream>
#include <span>
#include <sstream>
#include <string>

bool safe(const std::string& report_str) {
  std::istringstream iss2(report_str);
  int n, prev;
  bool inc = true, dec = true;
  for (int i = 0; iss2 >> n; i++) {
    if (i > 0) {
      if (abs(n - prev) > 3 || abs(n - prev) < 1)
        return false;
      inc = inc && n > prev;
      dec = dec && n < prev;
    }
    prev = n;
  }
  return inc || dec;
}

int Run(const std::string& input) {
  std::istringstream iss(input);
  int safe_count = 0;
  for (std::string line; std::getline(iss, line);) {
    if (safe(line)) safe_count++;
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
