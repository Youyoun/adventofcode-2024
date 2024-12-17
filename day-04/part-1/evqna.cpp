#include <chrono>
#include <iostream>
#include <span>
#include <sstream>
#include <string>
#include <string_view>
#include <vector>

using Grid = std::vector<std::string>;

int count_occurences(const Grid& g, const std::string_view target) {
  int H = g.size(), W = g[0].size();
  int count = 0;
  for (int i = 0; i < H; i++) {
    for (int j = 0; j < W; j++) {
      int DELTAS[][2] = {{+1, 0},  {-1, 0},  {0, +1},  {0, -1},
                         {+1, +1}, {-1, +1}, {+1, -1}, {-1, -1}};
      for (const auto delta : DELTAS) {
        int i2 = i, j2 = j;
        bool match = true;
        for (char c : target) {
          if (!(0 <= i2 && i2 < H && 0 <= j2 && j2 < W && g[i2][j2] == c)) {
            match = false;
            break;
          }
          i2 += delta[0];
          j2 += delta[1];
        }
        if (match) count++;
      }
    }
  }
  return count;
}

int Run(const std::string& input) {
  Grid grid;
  std::istringstream iss(input);
  for (std::string line; std::getline(iss, line);) {
    grid.push_back(line);
  }
  return count_occurences(grid, "XMAS");
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
