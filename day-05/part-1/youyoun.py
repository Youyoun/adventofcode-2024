from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):
    def run(self, s: str):
        """
        :param s: input in string format
        :return: solution flag
        """
        ordering, updates = [s2.split("\n") for s2 in s.split("\n\n")]
        order_map = {}
        for line in ordering:
            page1, page2 = line.split("|")
            if page1 not in order_map:
                order_map[page1] = {"before": set(), "after": set()}
            if page2 not in order_map:
                order_map[page2] = {"before": set(), "after": set()}
            order_map[page1]["after"].add(page2)
            order_map[page2]["before"].add(page1)
        count = 0
        for update in updates:
            is_in_right_order = True
            pages = update.split(",")
            for i in range(len(pages)):
                current_page = pages[i]
                if i > 0:
                    for prev_p in pages[:i]:
                        if prev_p not in order_map[current_page]["before"]:
                            is_in_right_order = False
                            break
                if i < len(pages) - 1:
                    for next_p in pages[i + 1 :]:
                        if next_p not in order_map[current_page]["after"]:
                            is_in_right_order = False
                            break
                if not is_in_right_order:
                    break
            if is_in_right_order:
                count += int(pages[len(pages) // 2])
        return count




def test_youyoun():
    """
    Run `python -m pytest ./day-05/part-1/youyoun.py` to test the submission.
    """
    assert (
        YouyounSubmission().run(
            """47|53
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
97,13,75,29,47""".strip()
        )
        == 143
    )
