#include <algorithm>
#include <chrono>
#include <iostream>
#include <queue>
#include <span>
#include <sstream>
#include <string>
#include <vector>

struct Disk {
  std::vector<int> sectors;

  static Disk FromMap(const std::string& m) {
    Disk d;
    int fid = 0;
    bool is_file = true;
    for (const char c : m) {
      int n = c - '0';
      std::vector<int> block;
      if (is_file) {
        block = std::vector<int>(n, fid++);
      } else if (n > 0) {
        block = std::vector<int>(n, -1);
      }
      d.sectors.insert(d.sectors.end(), block.begin(), block.end());
      is_file = !is_file;
    }
    return d;
  }

  void compress() {
    size_t i = 0, j = sectors.size() - 1;
    while (i < j) {
      while (sectors[i] >= 0) {
        i++;
      }
      while (i < j && sectors[j] < 0) {
        j--;
      }
      while (i < j && sectors[i] < 0 && sectors[j] >= 0) {
        std::swap(sectors[i++], sectors[j--]);
      }
    }
  }

  int64_t checksum() const {
    int64_t sum = 0;
    for (size_t i = 0; i < sectors.size(); i++)
      if (sectors[i] > 0) sum += i * sectors[i];
    return sum;
  }
};

auto Run(const std::string& input) {
  Disk d = Disk::FromMap(input);
  d.compress();
  return d.checksum();
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
