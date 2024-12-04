#include <chrono>
#include <iostream>
#include <span>
#include <sstream>
#include <string>
#include <string_view>
#include <vector>

using Grid = std::vector<std::string>;

bool x_match(const Grid& g, int i, int j, int H, int W) {
  auto check = [&g, H, W](int i, int j, char c) {
    return 0 <= i && i < H && 0 <= j && j < W && g[i][j] == c;
  };
  if (!check(i, j, 'A'))  return false;
  bool diag1 = (check(i - 1, j - 1, 'M') && check(i + 1, j + 1, 'S')) ||
               (check(i - 1, j - 1, 'S') && check(i + 1, j + 1, 'M'));
  bool diag2 = (check(i - 1, j + 1, 'M') && check(i + 1, j - 1, 'S')) ||
               (check(i - 1, j + 1, 'S') && check(i + 1, j - 1, 'M'));
  return diag1 && diag2;
}

int count_occurences(const Grid& grid) {
  int H = grid.size(), W = grid[0].size();
  int count = 0;
  for (int i = 1; i < H - 1; i++) {
    for (int j = 1; j < W - 1; j++) {
      if (x_match(grid, i, j, H, W)) count++;
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
  return count_occurences(grid);
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
