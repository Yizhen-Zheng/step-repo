from wikipedia_1 import Wikipedia


# ------------Test Cases------------


def test_with_s():
    w = Wikipedia('small')
    test_find_shortest_path(w, 'C', 'F')
    test_find_shortest_path(w, 'A', 'C')
    test_find_shortest_path(w, 'B', 'C')
    test_find_most_popular_pages(w)


def test_with_m():
    w = Wikipedia('medium')
    test_find_shortest_path(w, "渋谷", "パレートの法則")
    test_find_shortest_path(w, "渋谷", "小野妹子")
    test_find_shortest_path(w, "渋谷", "新宿区")
    test_find_shortest_path(w, "渋谷", "新宿")
    test_find_shortest_path(w, "渋谷", "渋谷")
    test_find_shortest_path(w, "渋谷", "渋谷区")
    test_find_shortest_path(w, "渋谷区", "渋谷")
    test_find_shortest_path(w, "渋谷区", "渋谷区")
    test_find_most_popular_pages(w)


def test_with_l():
    w = Wikipedia('large')
    test_find_shortest_path(w, "渋谷", "パレートの法則")
    test_find_shortest_path(w, "渋谷", "小野妹子")

# ------------Test Function------------


def test_find_shortest_path(w: Wikipedia, start, goal):
    res = w.find_shortest_path(start, goal)
    print(res)
    return


def test_find_most_popular_pages(w: Wikipedia):
    top_pages = w.find_most_popular_pages()
    print(item for item in w.page_rank.items())
    print(top_pages)
    return

# ------------Driver code------------


def run_test():
    test_with_s()
    test_with_m()
    # cache l cost 2.3 GB ram
    # test_with_l()


if __name__ == '__main__':
    run_test()
