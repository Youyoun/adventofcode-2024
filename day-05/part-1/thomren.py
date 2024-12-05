from collections import defaultdict
from tool.runners.python import SubmissionPy


class ThomrenSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        dependencies_str, updates_str = s.split("\n\n")

        dependencies = defaultdict(set)
        for line in dependencies_str.splitlines():
            a, b = line.split("|")
            dependencies[b].add(a)

        res = 0
        for update in updates_str.splitlines():
            pages = update.split(",")
            if self.is_ordering_right(pages, dependencies):
                res += int(pages[len(pages) // 2])
        return res

    @staticmethod
    def is_ordering_right(pages: list[str], dependencies: dict[str, set[str]]) -> bool:
        done = set()
        for page in pages:
            if not (dependencies[page] & set(pages)).issubset(done):
                return False
            done.add(page)
        return True


def test_thomren():
    """
    Run `python -m pytest ./day-05/part-1/thomren.py` to test the submission.
    """
    assert (
        ThomrenSubmission().run(
            """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""".strip()
        )
        == 143
    )
