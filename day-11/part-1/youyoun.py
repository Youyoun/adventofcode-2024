import functools

from tool.runners.python import SubmissionPy

@functools.cache
def count_splits(n, n_blinks=25):
    if n_blinks == 0:
        return 1
    if n == 0:
        return count_splits(1, n_blinks=n_blinks-1)
    elif (n_len := len((n_str := str(n)))) % 2 == 0:
        return count_splits(int(n_str[:n_len // 2]), n_blinks=n_blinks-1) + count_splits(int(n_str[n_len // 2:]), n_blinks=n_blinks-1)
    return count_splits(n * 2024, n_blinks=n_blinks-1)



class YouyounSubmission(SubmissionPy):
    def run(self, s: str, n_blinks=25):
        """
        :param s: input in string format
        :return: solution flag
        """
        s = list(map(int, s.split(" ")))
        return sum(count_splits(n, n_blinks=n_blinks) for n in s)
