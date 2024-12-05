#include <algorithm>
#include <chrono>
#include <iostream>
#include <span>
#include <sstream>
#include <string>
#include <vector>

// Maybe in C++ 36  ¯\_(ツ)_/¯
std::vector<int> split(const std::string& s, char delim) {
  std::vector<int> result;
  std::istringstream iss(s);
  for (std::string item; std::getline(iss, item, delim);) {
    result.push_back(std::stoi(item));
  }
  return result;
}

bool contains(const std::vector<int>& V, int x) {
  return std::find(V.begin(), V.end(), x) != V.end();
}

using Lookup = std::vector<std::vector<int>>;

bool valid(const std::vector<int>& update, const Lookup& rules) {
  for (size_t i = 0; i < update.size(); i++) {
    for (size_t j = i + 1; j < update.size(); j++) {
      if (contains(rules[update[j]], update[i]))
        return false;
    }
  }
  return true;
}

int Run(const std::string& input) {
  int i = input.find("\n\n");
  std::istringstream rule_iss(input.substr(0, i));
  std::istringstream update_iss(input.substr(i + 2, std::string::npos));
  std::string line;

  Lookup rules(100);
  while (std::getline(rule_iss, line)) {
    int a, b;
    sscanf(line.c_str(), "%d|%d", &a, &b);
    rules[a].push_back(b);
  }

  int sum = 0;
  while (std::getline(update_iss, line)) {
    std::vector<int> update = split(line, ',');
    if (valid(update, rules)) {
      int midpoint = update.size() / 2;
      sum += update[midpoint];
    }
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
