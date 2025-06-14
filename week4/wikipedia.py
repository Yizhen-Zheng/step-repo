import sys
import collections
import pickle
import os


class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file, cache_file='wikipedia_cache'):
        '''
        path: starts with cd into ./week4
        self.pages_file: path to page ID to page title 
        self.links_file = path to page ID to links
        self.cache_file = path to pickle cache file(handle multiple run time)
        self.titles: 
            A dict, mapping from a page ID (integer) to the page title.
            For example, self.titles[1234] returns the title of the page whose
            ID is 1234.
        self.links:
            A dict, whose key is page ID, value is a adj list of page links from the page.
            For example, self.links[1234] returns a list contains all destination pages linked from page[1234]
        '''

        self.pages_file = pages_file
        self.links_file = links_file
        self.cache_file = cache_file

        self.titles = {}
        self.links = {}

        if os.path.exists(cache_file):
            print(f'loading from cache: {cache_file}')
            self._load_from_cache()
        else:
            print("Cache not found, reading from text files...")
            self._read_files()
            self._save_to_cache()

    def _read_files(self):
        with open(self.pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % self.pages_file)

        with open(self.links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                self.links[src].append(dst)
        print("Finished reading %s" % self.links_file)

    def _save_to_cache(self):
        print("Saving to cache...")
        with open(self.cache_file, 'wb') as f:
            pickle.dump({'titles': self.titles, 'links': self.links}, f)
        print("Cache saved!")

    def _load_from_cache(self):
        with open(self.cache_file, 'rb') as f:
            data = pickle.load(f)
            self.titles = data['titles']
            self.links = data['links']
        print("Loaded from cache successfully!")

    def find_longest_titles(self):
        '''Example: Find the longest titles.'''
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()

    def find_most_linked_pages(self):
        '''
        Example: Find the most linked pages.
        loops all links, count how many time the page is linked from others
        O(E)
        '''
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    def find_shortest_path(self, start, goal):
        '''
        'start': A title of the start page.
        'goal': A title of the goal page.

        '''
        pages = collections.deque([start])
        while len(pages):
            current_page = pages.popleft()
        pass

    # Homework #2: Calculate the page ranks and print the most popular pages.

    def find_most_popular_pages(self):
        # ------------------------#
        # Write your code here!  #
        # ------------------------#
        pass

    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.

    def find_longest_path(self, start, goal):
        # ------------------------#
        # Write your code here!  #
        # ------------------------#
        pass

    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.

    def assert_path(self, path, start, goal):
        assert (start != goal)
        assert (len(path) >= 2)
        assert (self.titles[path[0]] == start)
        assert (self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert (path[i + 1] in self.links[path[i]])


if __name__ == "__main__":
    PATHS = [('./wikipedia_dataset/pages_small.txt', './wikipedia_dataset/links_small.txt', 'wikipedia_s.pkl'), ('./wikipedia_dataset/pages_medium.txt', './wikipedia_dataset/links_medium.txt', 'wikipedia_m.pkl'), ('./wikipedia_dataset/pages_large.txt',
                                                                                                                                                                                                                      './wikipedia_dataset/links_large.txt', 'wikipedia_l.pkl')]
    if len(sys.argv) != 2:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)
    # hanlde invalid input
    choice = int(sys.argv[1])
    data_path = PATHS[choice]
    wikipedia = Wikipedia(data_path[0], data_path[1], data_path[2])
    # examples
    wikipedia.find_longest_titles()
    wikipedia.find_most_linked_pages()
    # Homework #1
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    wikipedia.find_longest_path("渋谷", "池袋")
