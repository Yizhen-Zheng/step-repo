import sys
import collections
import pickle
import os
import sqlite3


class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, dataset_size='small'):
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
        file_path = {
            'small': ('wikipedia_dataset/pages_small.txt', 'wikipedia_dataset/links_small.txt', 'wikipedia_s.pkl', 'relevant_pages_s.pkl'),
            'medium': ('wikipedia_dataset/pages_medium.txt', 'wikipedia_dataset/links_medium.txt', 'wikipedia_m.pkl', 'relevant_pages_m.pkl'),
            'large': ('wikipedia_dataset/pages_large.txt', 'wikipedia_dataset/links_large.txt', 'wikipedia_l.pkl', 'relevant_pages_l.pkl')
        }
        if dataset_size not in file_path:
            raise ValueError(
                f"Invalid dataset size '{dataset_size}'. Please use 'small', 'medium', or 'large'.")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        pages_file, links_file, cache_file, relevant_pages_file = [
            os.path.join(base_dir, e) for e in file_path[dataset_size]]

        self.pages_file = pages_file
        self.links_file = links_file
        self.cache_file = cache_file
        self.relevant_pages_file = relevant_pages_file

        self.titles = {}
        self.links = {}
        self.links_reversed = collections.defaultdict(list)
        self.relevant_pages = set()
        self.THRESHOLD = 0.01
        self.DAMPING = 0.85

        # if False:
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

        # initialize reversed links (store pages as {dst:[srcs]})
        for src, dsts in self.links.items():
            for dst in dsts:
                self.links_reversed[dst].append(src)

        print("Finished reading %s" % self.links_file)

    def _save_to_cache(self):
        print("Saving to cache...")
        with open(self.cache_file, 'wb') as f:
            pickle.dump({'titles': self.titles, 'links': self.links, 'links_reversed': self.links_reversed}, f)
        print("Cache saved!")

    def _load_from_cache(self):
        with open(self.cache_file, 'rb') as f:
            data = pickle.load(f)
            self.titles = data['titles']
            self.links = data['links']
            self.links_reversed = data['links_reversed']
        print("Loaded from cache successfully!")

    def find_id_by_title(self, target_title):
        '''
        input: the page title 
        return: page id of that page
        '''
        pageid = [id for id, title in self.titles.items() if title ==
                  target_title]
        if not len(pageid):
            print(
                f'page not found: {target_title}\nplease change dataset size or change title')
            return -1
        return pageid[0]

    def find_shortest_path(self, start, goal):
        '''
        'start': A title of the start page.
        'goal': A title of the goal page.
        '''
        start_id = self.find_id_by_title(start)
        goal_id = self.find_id_by_title(goal)

        pages = collections.deque([start_id])
        visited = {start_id: 0}

        while len(pages):
            current_pageid = pages.popleft()
            current_step_count = visited[current_pageid]
            if current_pageid == goal_id:
                return current_step_count
            neighbors = self.links[current_pageid]
            for neighbor in neighbors:
                if not neighbor in visited:
                    pages.append(neighbor)
                    visited[neighbor] = current_step_count+1

        return -1

    def _find_reachable_to(self, goal_id):
        '''detect all pages that can reach goal'''
        visited = {goal_id}
        queue = collections.deque([goal_id])

        while queue:
            current = queue.popleft()
            for src in self.links_reversed[current]:
                if src not in visited:
                    queue.append(src)
                    visited.add(src)
        return visited

    def _find_reachable_from(self, start_id):
        '''detect all pages that can be reached from start'''
        visited = {start_id}
        queue = collections.deque([start_id])
        while queue:
            current = queue.popleft()
            # since dict self.link has been already write into pkl, i used get with defaul value
            for dst in self.links.get(current, []):
                if dst not in visited:
                    queue.append(dst)
                    visited.add(dst)

        return visited

    def _prepare_longest_path(self, start_id, goal_id):
        '''
        replace self.links with cleaned pages(remove dead end). doesn't effect much (reduce about 1/5 irrelevant pages) '''
        print(self.relevant_pages)
        if os.path.exists(self.relevant_pages_file):
            print(f'loading from cache: {self.relevant_pages_file}')
            with open(self.relevant_pages_file, 'rb') as f:
                data = pickle.load(f)
                self.relevant_pages = data['relevant_pages']
        else:
            reachable_to_goal = self._find_reachable_to(goal_id)
            reachable_from_start = self._find_reachable_from(start_id)
            relevant_pages = reachable_to_goal & reachable_from_start
            with open(self.relevant_pages_file, 'wb')as f:
                pickle.dump({'relevant_pages': relevant_pages}, f)
        print(len(self.relevant_pages), '/', len(self.links))
        self.links = {key: value for key, value in self.links.items() if key in self.relevant_pages}
        return

    def find_longest_path_1(self, start, goal):
        '''
        Search the longest path with heuristics.
        'start': A title of the start page.
        'goal': A title of the goal page.
        it works for samll, and take too much memory for medium that havn't seen result
        there should be ways to reduce memory usage
        '''
        start_id = self.find_id_by_title(start)
        goal_id = self.find_id_by_title(goal)
        self._prepare_longest_path(start_id, goal_id)
        longest_path = []
        iteration_count = 0
        # (current node, current path, current visited)
        stack = [(start_id, [start_id], {start_id})]
        while stack:
            iteration_count += 1
            if iteration_count % 1000 == 0:
                print(f'iterations:{iteration_count}\nStack size: {len(stack)}\nLongest path:{len(longest_path)} ')
            current, path, visited = stack.pop()

            if current == goal_id:
                if len(path) > len(longest_path):
                    longest_path = path
                    print(f'new longest: {len(longest_path)}')
                continue
            for neighbor in reversed(self.links.get(current, [])):
                if neighbor not in visited:
                    new_visited = visited.copy()
                    new_visited.add(neighbor)
                    stack.append((neighbor, path+[neighbor], new_visited))

        return longest_path

    def find_longest_path_2(self, start, goal):
        '''
        random walk, longest find in medium: 1709. doesn't work well
        '''
        start_id = self.find_id_by_title(start)
        goal_id = self.find_id_by_title(goal)
        self._prepare_longest_path(start_id, goal_id)
        longest_path = []

        # (current node, current path, current visited)
        for i in range(1000000):
            if i % 1000 == 0:
                print(f'{i} iterations, longest: {len(longest_path)}')
            path = self.random_walk(start_id, goal_id)

            if path:
                if len(path) > len(longest_path):
                    longest_path = path
                    print(f'new longest:{len(path)}')
                else:
                    print(f'new path:{len(path)}')
        return longest_path

    def random_walk(self, start_id, goal_id):
        import random
        current = start_id
        path = [start_id]
        visited = {start_id}
        for _ in range(495590):
            if current == goal_id:
                return path

            neighbors = [n for n in self.links.get(current, []) if n not in visited]
            if not neighbors:
                return None
            next_page = random.choice(neighbors)
            path.append(next_page)
            visited.add(next_page)
            current = next_page
        return path

    def assert_path(self, path, start, goal):
        '''
        a helper function for Homework #3, 
        use this function to check if the found path is well formed.
        'path': An array of page IDs that stores the found path.
            path[0] is the start page. path[-1] is the goal page.
            path[0] -> path[1] -> ... -> path[-1] is the path from the start page to the goal page.
        'start': A title of the start page.
        'goal': A title of the goal page.
        '''
        assert (start != goal)
        assert (len(path) >= 2)
        assert (self.titles[path[0]] == start)
        assert (self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert (path[i + 1] in self.links[path[i]])


if __name__ == "__main__":
    print('please select which dataset you want to use', end='\n')
    dataset_size = input().strip()
    wikipedia = Wikipedia(dataset_size)

    # wikipedia.find_longest_path("渋谷", "池袋")
