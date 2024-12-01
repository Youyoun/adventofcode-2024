#include <algorithm>
#include <chrono>
#include <iostream>
#include <span>
#include <sstream>
#include <string>
#include <vector>

int Run(const std::string& input) {
  std::istringstream iss(input);
  std::vector<int> L, R;
  for (std::string line; std::getline(iss, line);) {
    int l, r;
    sscanf(line.c_str(), "%d %d", &l, &r);
    L.push_back(l);
    R.push_back(r);
  }

  std::sort(L.begin(), L.end());
  std::sort(R.begin(), R.end());
  int distance = 0;
  for (size_t i = 0; i < L.size(); i++)
    distance += abs(L[i] - R[i]);
  return distance;
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
