#include <chrono>
#include <iostream>
#include <span>
#include <sstream>
#include <string>
#include <vector>

struct Block {
  int begin, end;
  int size() const { return end - begin; }
};

struct File {
  int id;
  Block block;
};

struct Disk {
  std::vector<File> files;
  std::vector<Block> free_list;

  static Disk FromMap(const std::string& m) {
    Disk d;
    int fid = 0, k = 0;
    bool is_file = true;
    for (const char c : m) {
      int n = c - '0';
      Block block{k, k + n};
      if (is_file) {
        d.files.push_back(File{fid++, block});
      } else if (n > 0) {
        d.free_list.push_back(block);
      }
      k += n;
      is_file = !is_file;
    }
    return d;
  }

  void compress() {
    for (int fid = files.size() - 1; fid >= 0; fid--) {
      File& f = files[fid];
      int s = f.block.size();
      for (Block& free_block : free_list) {
        if (free_block.begin >= f.block.begin)  break;
        if (free_block.size() >= s) {
          f.block = Block{free_block.begin, free_block.begin + s};
          free_block.begin += s;
          break;
        }
      }
    }
  }

  int64_t checksum() const {
    int64_t sum = 0;
    for (const File& f : files)
      for (int i = f.block.begin; i < f.block.end; i++)
        sum += i * f.id;
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
  // auto answer = Run("2333133121414131402");
  auto end = std::chrono::high_resolution_clock::now();

  std::cout << "_duration:"
            << std::chrono::duration<float, std::milli>(end - start).count()
            << "\n";

  std::cout << answer << "\n";
  return 0;
}
