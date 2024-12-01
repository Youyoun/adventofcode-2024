#include <algorithm>
#include <chrono>
#include <iostream>
#include <span>
#include <sstream>
#include <string>
#include <vector>

int count_consecutive(const std::vector<int>& V, size_t i, int x) {
  int c = 0;
  while (i < V.size() && V[i++] == x) c++;
  return c;
}

int similarity(const std::vector<int>& A, const std::vector<int>& B) {
  int S = 0;
  size_t i = 0, j = 0, N = A.size(), M = B.size();
  while (i < N && j < M) {
    // Advance to next A[i] == B[j] position
    while (i < N && j < M && A[i] != B[j]) {
      if (A[i] < B[j])  i++;
      else if (A[i] > B[j])  j++;
    }
    // Compute similarity for this value
    if (i < N && j < M) {
      int x = A[i];
      int l = count_consecutive(A, i, x);
      int r = count_consecutive(B, j, x);
      S += x * l * r;
      i += l; j += r;
    }
  }
  return S;
}

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
  return similarity(L, R);
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
