from wikipedia_2 import Wikipedia


# ------------Test Cases------------

def test_with_s():
    w = Wikipedia('small')
    # test_find_longest_path(w, 'C', 'C')  # 0
    test_find_longest_path(w, 'C', 'F')  # 5


def test_with_m():
    w = Wikipedia('medium')
    test_find_longest_path(w, '渋谷', '池袋')


def test_with_l():
    w = Wikipedia('large')
    test_find_longest_path(w, '渋谷', '池袋')


# ------------Test Function------------


def test_find_longest_path(w: Wikipedia, start, goal):
    # path = w.find_longest_path_1(start, goal)
    path = w.find_longest_path_2(start, goal)
    print(path)
    return

# ------------Driver code------------


def run_test():
    test_with_s()
    # test_with_m()
    # cache l cost 2.3 GB ram
    # test_with_l()


if __name__ == '__main__':
    run_test()
