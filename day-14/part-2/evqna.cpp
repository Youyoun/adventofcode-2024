#include <chrono>
#include <iostream>
#include <span>
#include <sstream>
#include <string>
#include <vector>

const int W = 101, H = 103;
const int MAX_TICKS = 10000;

struct Vec2 {
  int x, y;
  Vec2 operator+(const Vec2 o) const { return {x + o.x, y + o.y}; }
};

struct Robot {
  Vec2 pos, mov;
};

void simulate(std::vector<Robot>& robots, int ticks) {
  for (Robot& r : robots) {
    r.pos.x = (r.pos.x + ticks * r.mov.x) % W;
    if (r.pos.x < 0) r.pos.x += W;
    r.pos.y = (r.pos.y + ticks * r.mov.y) % H;
    if (r.pos.y < 0) r.pos.y += H;
  }
}

int nb_neighbors(const std::vector<int>& grid, Vec2 pos) {
  auto has_robot = [&grid](Vec2 p) {
    return 0 <= p.x && p.x < W && 0 <= p.y && p.y < H &&
           grid[p.x + W * p.y] > 0;
  };
  const Vec2 DELTAS[] = {{0, +1}, {0, -1}, {+1, 0}, {-1, 0}};
  int count = 0;
  for (const Vec2 delta : DELTAS)
    if (has_robot(pos + delta)) count++;
  return count;
}

int isolation_score(const std::vector<Robot>& robots) {
  std::vector<int> grid(W * H);
  for (const Robot& r : robots) grid[r.pos.x + W * r.pos.y]++;

  int isolated = 0;
  for (const Robot& r : robots) {
    if (!nb_neighbors(grid, r.pos)) isolated++;
  }
  return isolated;
}

void display(const std::vector<Robot>& robots) {
  std::vector<int> grid(W * H);
  for (const Robot& r : robots) grid[r.pos.x + W * r.pos.y]++;
  for (int y = 0; y < H; y++) {
    std::string line(W, '.');
    for (int x = 0; x < W; x++) {
      if (grid[x + W * y] > 0) line[x] = std::to_string(grid[x + W * y])[0];
    }
    std::cout << line << "\n";
  }
  std::cout << std::endl;
}

auto Run(const std::string& input) {
  std::istringstream iss(input);
  std::vector<Robot> robots;
  for (std::string line; std::getline(iss, line);) {
    int x, y, dx, dy;
    sscanf(line.c_str(), "p=%d,%d v=%d,%d", &x, &y, &dx, &dy);
    robots.push_back({{x, y}, {dx, dy}});
  }

  int min_score = INT32_MAX, min_tick;
  for (int tick = 1; tick < MAX_TICKS; tick++) {
    int step = 1;
    simulate(robots, step);
    int is = isolation_score(robots);
    if (is < min_score) {
      min_score = is;
      min_tick = tick;
    }
  }
  return min_tick;
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
