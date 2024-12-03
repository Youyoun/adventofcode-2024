#include <chrono>
#include <iostream>
#include <regex>
#include <span>
#include <sstream>
#include <string>

int Run(const std::string& input) {
  std::regex re(R"(mul\((\d+),(\d+)\))");
  std::sregex_iterator begin(input.begin(), input.end(), re);
  std::sregex_iterator end;
  int sum = 0;
  for (std::sregex_iterator it = begin; it != end; ++it) {
    int a = std::stoi(it->str(1)), b = std::stoi(it->str(2));
    sum += a * b;
  }
  return sum;
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
