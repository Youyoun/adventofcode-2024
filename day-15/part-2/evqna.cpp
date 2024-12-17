#include <chrono>
#include <iostream>
#include <queue>
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

  void dbg() const {
    for (const auto& line : grid)
      std::cout << line << "\n";
  }

  Vec2 box_pos(Vec2 p) {
    if (at(p) == '[')
      return p;
    else if (at(p) == ']')
      return p + Vec2{0, -1};
    return {-1, -1};
  }

  void move_bot(Vec2 dir) {
    std::vector<Vec2> boxes;
    Vec2 pos = bot + dir;
    bool can_move = true;
    if (dir.i == 0) {
      // Horizontal move
      while (at(pos) == '[' || at(pos) == ']') {
        boxes.push_back(box_pos(pos));
        pos = pos + dir + dir;
      }
      can_move = at(pos) == '.';
    } else if (dir.j == 0) {
      // Vertical move
      std::queue<Vec2> cur;
      cur.push(pos);
      while (!cur.empty()) {
        Vec2 p = cur.front();
        if (at(p) == '#')
          return;
        if (at(p) == '[' || at(p) == ']') {
          Vec2 b = box_pos(p);
          boxes.push_back(b);
          cur.push(b + dir);
          cur.push(b + Vec2{0, 1} + dir);
        }
        cur.pop();
      }      
    }

    if (can_move) {
      for (Vec2 b : boxes) {
        at(b) = '.';
        at(b + Vec2{0, 1}) = '.';
      }
      for (Vec2 b : boxes) {
        at(b + dir) = '[';
        at(b + Vec2{0, 1} + dir) = ']';
      }
      at(bot) = '.';
      bot = bot + dir;
      at(bot) = '@';
    }
  }

  int gps() const {
    int total = 0;
    for (size_t i = 0; i < grid.size(); i++)
      for (size_t j = 0; j < grid[i].size(); j++)
        if (grid[i][j] == '[')
          total += 100 * (int)i + (int)j;
    return total;
  }
};

std::vector<std::string> expand(const std::vector<std::string>& g) {
  std::vector<std::string> e(g.size());
  for (size_t i = 0; i < g.size(); i++) {
    for (size_t j = 0; j < g[i].size(); j++) {
      if (g[i][j] == '#')
        e[i] += "##";
      else if (g[i][j] == '.')
        e[i] += "..";
      else if (g[i][j] == 'O')
        e[i] += "[]";
      else if (g[i][j] == '@')
        e[i] += "@.";
    }
  }
  return e;
}

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

  Warehouse w(expand(grid));
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
      // w.dbg();
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
