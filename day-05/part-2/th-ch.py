from tool.runners.python import SubmissionPy

from collections import defaultdict


class ThChSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        rules, updates = s.split("\n\n")
        ordering = defaultdict(set)
        for rule in rules.split("\n"):
            p1, p2 = rule.split("|")
            ordering[int(p1)].add(int(p2))

        middle_pages = []

        for update in updates.split("\n"):
            pages = list(map(int, update.split(",")))
            is_valid = True
            for i in range(len(pages)):
                for j in range(i + 1, len(pages)):
                    if pages[i] in ordering[pages[j]]:
                        is_valid = False
                        break
                if not is_valid:
                    break

            if is_valid:
                continue

            after_page = dict()
            for page in pages:
                other_pages = set(pages) - {page}
                after_page[page] = len(other_pages.intersection(ordering[page]))
            sorted_page = sorted(after_page.keys(), key=lambda p: after_page[p], reverse=True)
            middle_pages.append(sorted_page[len(pages) // 2])

        return sum(middle_pages)


def test_th_ch():
    """
    Run `python -m pytest ./day-05/part-2/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
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
