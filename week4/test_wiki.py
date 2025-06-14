from wikipedia import Wikipedia, PATHS


def test_with_s():
    w = Wikipedia(PATHS[0][0], PATHS[0][1], PATHS[0][2])
    test_find_shortest_path(w, 'C', 'F')
    test_find_shortest_path(w, 'A', 'C')
    test_find_shortest_path(w, 'B', 'C')


def test_with_m():
    w = Wikipedia(PATHS[1][0], PATHS[1][1], PATHS[1][2])


def test_with_l():
    w = Wikipedia(PATHS[2][0], PATHS[2][1], PATHS[2][2])


def test_find_shortest_path(w: Wikipedia, start, goal):
    res = w.find_shortest_path(start, goal)
    print(res)
    return


def test_find_most_popular_pages(w: Wikipedia):
    return


def run_test():
    '''
    driver code
    '''
    test_with_s()
    # test_with_m()
    # cache l cost 2.3 GB ram
    # test_with_l()


if __name__ == '__main__':
    run_test()
