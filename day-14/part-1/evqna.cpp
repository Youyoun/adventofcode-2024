#include <chrono>
#include <iostream>
#include <span>
#include <sstream>
#include <string>
#include <vector>

const int W = 101, H = 103;
const int TICKS = 100;

struct Vec2 {
  int x, y;
};

struct Robot {
  Vec2 pos, mov;
};

void simulate(std::vector<Robot>& robots, int ticks) {
  for (Robot& r : robots) {
    r.pos.x = (r.pos.x + ticks * r.mov.x) % W;
    if (r.pos.x < 0)  r.pos.x += W;
    r.pos.y = (r.pos.y + ticks * r.mov.y) % H;
    if (r.pos.y < 0)  r.pos.y += H;
  }
}

int safety_factor(const std::vector<Robot>& robots) {
  int ne = 0, se = 0, sw = 0, nw = 0;
  for (const Robot& r : robots) {
    if (r.pos.x < W / 2) {
      if (r.pos.y < H / 2)
        nw++;
      else if (r.pos.y > H / 2)
        sw++;
    } else if (r.pos.x > W / 2) {
      if (r.pos.y < H / 2)
        ne++;
      else if (r.pos.y > H / 2)
        se++;
    }
  }
  return ne * se * sw * nw;
}

auto Run(const std::string& input) {
  std::istringstream iss(input);
  std::vector<Robot> robots;
  for (std::string line; std::getline(iss, line);) {
    int x, y, dx, dy;
    sscanf(line.c_str(), "p=%d,%d v=%d,%d", &x, &y, &dx, &dy);
    robots.push_back({{x, y}, {dx, dy}});
  }

  simulate(robots, TICKS);
  return safety_factor(robots);
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
