#include <chrono>
#include <iostream>
#include <span>
#include <sstream>
#include <string>
#include <vector>

struct Vec2 {
  int i, j;
  Vec2 operator+(const Vec2 o) const { return {i + o.i, j + o.j}; }
};

struct Warehouse {
  std::vector<std::string> grid;
  Vec2 bot;

  Warehouse(std::vector<std::string> grid_in) : grid(grid_in) {
    for (size_t i = 0; i < grid.size(); i++) {
      for (size_t j = 0; j < grid[i].size(); j++) {
        if (grid[i][j] == '@') {
          bot = Vec2{(int)i, (int)j};
          return;
        }
      }
    }
  }

  char& at(Vec2 p) {
    return grid[p.i][p.j];
  }

  void move_bot(Vec2 dir) {
    Vec2 pos = bot + dir;
    while (at(pos) == 'O')
      pos = pos + dir;
    if (at(pos) == '.') {
      at(bot) = '.';
      if (at(bot + dir) == 'O')
        at(pos) = 'O';
      bot = bot + dir;
      at(bot) = '@';
    }
  }

  int gps() const {
    int total = 0;
    for (size_t i = 0; i < grid.size(); i++)
      for (size_t j = 0; j < grid[i].size(); j++)
        if (grid[i][j] == 'O')
          total += 100 * (int)i + (int)j;
    return total;
  }
};

auto Run(const std::string& input) {
  std::istringstream iss(input);
  std::vector<std::string> grid;
  std::vector<std::string> moves;
  bool is_grid = true;
  for (std::string line; std::getline(iss, line);) {
    if (line.empty()) {
      is_grid = false;
      continue;
    }
    if (is_grid)
      grid.push_back(line);
    else
      moves.push_back(line);
  }

  Warehouse w(grid);
  for (const auto& line : moves) {
    for (char c : line) {
      if (c == '^')
        w.move_bot({-1, 0});
      else if (c == '>')
        w.move_bot({0, +1});
      else if (c == 'v')
        w.move_bot({+1, 0});
      else if (c == '<')
        w.move_bot({0, -1});
    }
  }
  return w.gps();
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
