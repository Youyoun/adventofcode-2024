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
            if not self.is_ordering_right(pages, dependencies):
                ordered_pages = self.sort_pages(pages, dependencies)
                res += int(ordered_pages[len(pages) // 2])
        return res

    @staticmethod
    def is_ordering_right(pages: list[str], dependencies: dict[str, set[str]]) -> bool:
        done = set()
        for page in pages:
            if not (dependencies[page] & set(pages)).issubset(done):
                return False
            done.add(page)
        return True

    @staticmethod
    def sort_pages(pages: list[str], dependencies: dict[str, set[str]]) -> list[str]:
        remaining_deps = {page: dependencies[page] & set(pages) for page in pages}
        ready = [page for page, deps in remaining_deps.items() if not deps]
        ordered_pages = []
        while ready:
            page = ready.pop()
            ordered_pages.append(page)
            remaining_deps.pop(page)
            for p in remaining_deps:
                remaining_deps[p].discard(page)
            ready.extend(page for page, deps in remaining_deps.items() if not deps)
        return ordered_pages


def test_thomren():
    """
    Run `python -m pytest ./day-05/part-2/thomren.py` to test the submission.
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
        == 123
    )
