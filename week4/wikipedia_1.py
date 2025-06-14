import sys
import collections
import pickle
import os


class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, dataset_size='small'):
        '''
        Attributes:
        self.titles(dict): 
            mapping  page ID (integer) to page title(str).
        self.links(dict):
            mapping  page ID (integer) to list of linked pages(list).
        '''
        # Define file paths for different dataset sizes
        file_path = {
            'small': ('wikipedia_dataset/pages_small.txt', 'wikipedia_dataset/links_small.txt', 'wikipedia_s.pkl'),
            'medium': ('wikipedia_dataset/pages_medium.txt', 'wikipedia_dataset/links_medium.txt', 'wikipedia_m.pkl'),
            'large': ('wikipedia_dataset/pages_large.txt', 'wikipedia_dataset/links_large.txt', 'wikipedia_l.pkl')
        }
        if dataset_size not in file_path:
            raise ValueError(
                f"Invalid dataset size '{dataset_size}'. Please use 'small', 'medium', or 'large'.")
        # Get absolute paths for data files
        base_dir = os.path.dirname(os.path.abspath(__file__))
        pages_file, links_file, cache_file = [
            os.path.join(base_dir, e) for e in file_path[dataset_size]]

        self.pages_file = pages_file
        self.links_file = links_file
        self.cache_file = cache_file

        # Initialize data structures
        self.titles = {}
        self.links = {}
        self.page_rank = {}

        # PageRank algorithm parameters
        self.THRESHOLD = 0.01  # Convergence threshold
        self.DAMPING = 0.85  # Damping factor

        # Load data from cache if available, otherwise read from files
        if os.path.exists(cache_file):
            print(f'loading from cache: {cache_file}')
            self._load_from_cache()
        else:
            print("Cache not found, reading from text files...")
            self._read_files()
            self._save_to_cache()

        # Initialize PageRank scores to 1.0 for all pages
        for id, t in self.titles.items():
            self.page_rank[id] = 1

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
        """Save loaded data to pickle cache for faster future loading."""
        print("Saving to cache...")
        with open(self.cache_file, 'wb') as f:
            pickle.dump({'titles': self.titles, 'links': self.links}, f)
        print("Cache saved!")

    def _load_from_cache(self):
        """Load data from pickle cache."""
        with open(self.cache_file, 'rb') as f:
            data = pickle.load(f)
            self.titles = data['titles']
            self.links = data['links']
        print("Loaded from cache successfully!")

    def find_id_by_title(self, target_title):
        '''
        find the page ID for a given page title.
        args: target_title (str): The title of the page to find
        returns: int: Page ID if found, -1 if not found
        '''
        pageid = [id for id, title in self.titles.items() if title ==
                  target_title]
        if not len(pageid):
            print(
                f'page not found: {target_title}\nplease change dataset size or change title')
            return -1
        return pageid[0]

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

    def find_shortest_path(self, start, goal):
        '''
        breadth-first search to find the shortest path between two pages using    
        args:
            start (str): Title of the starting page
            goal (str): Title of the destination page 
        returns: int: length of shortest path, or -1 if no path exists

        O(V + E) where V is vertices and E is edges
        '''
        start_id = self.find_id_by_title(start)
        goal_id = self.find_id_by_title(goal)

        if start_id != -1 and goal_id != -1:
            pages = collections.deque([start_id])
            visited = {start_id: 0}

            while len(pages):
                current_pageid = pages.popleft()
                current_step_count = visited[current_pageid]
                if current_pageid == goal_id:
                    # check if reached the goal
                    return current_step_count
                # enqueue neighbors
                neighbors = self.links[current_pageid]
                for neighbor in neighbors:
                    if not neighbor in visited:
                        pages.append(neighbor)
                        visited[neighbor] = current_step_count+1

        return -1

    def find_most_popular_pages(self):
        '''
        Homework #2: Calculate the page ranks and print the most popular pages.
        1. all pages are initialized with rank 1.0
        2. iteratively update ranks withdamping factor
        3. Continue until convergence (sum of squared differences < threshold)

        O(n*(N+E)), while n is the iterate time
        PR(A) = (1-d)/N + d * Σ(PR(T)/C(T))
        - d = damping factor (0.85)
        - N = total number of pages
        - T = pages that link to A
        - C(T) = number of outbound links from T

        returns: list: Top 10 pages as (page_id, pagerank_score) tuples, sorted by score
        '''
        remain_factor = 1-self.DAMPING
        damping_factor = self.DAMPING

        converged = False
        while not converged:
            # initialize new empty page rank
            new_page_rank = {}
            for id, t in self.titles.items():
                new_page_rank[id] = 0

            total_score_to_damp = 0
            for id, t in self.titles.items():
                current_rank = self.page_rank[id]
                neighbors = self.links[id]
                # distribute rank to all linked pages
                for neighbor in neighbors:
                    new_page_rank[neighbor] += damping_factor * current_rank/len(neighbors)

                # Pages with no outbound links distribute rank to all pages
                total_score_to_damp += (remain_factor if neighbors else 1) * current_rank

            # distribute total_score_to_damp to all pages
            total_score_to_damp /= len(new_page_rank)
            for id, page_score in new_page_rank.items():
                new_page_rank[id] += total_score_to_damp
            converged = self._is_converged(new_page_rank)
            self.page_rank = new_page_rank
        # find top 10 pages
        top_pages = list(self.page_rank.items())
        top_pages = sorted(top_pages, key=lambda page: page[1], reverse=True)[:10]
        return top_pages

    def _is_converged(self, new_page_rank):
        '''
        compare self.page_rank with new_page_rank
        check if PageRank algorithm has converged by comparing old and new ranks.

        args: new_page_rank (dict): New PageRank scores to compare against current ones
        returns: bool: True if converged (sum of squared differences < threshold)
        '''
        sum_squared_difference = 0
        for pageid, new_score in new_page_rank.items():
            old_score = self.page_rank[pageid]
            sum_squared_difference += pow(new_score-old_score, 2)

        print(f'Sum of squared differences:{sum_squared_difference}')
        return sum_squared_difference < self.THRESHOLD

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
    '''
    dataset_size: small, medium, large
    '''
    print('please select which dataset you want to use', end='\n')
    dataset_size = input().strip().lower()
    wikipedia = Wikipedia(dataset_size)

    # choose 'small' and uncomment this line
    # wikipedia.find_shortest_path('A','C')

    # choose 'medium' and uncomment this line
    # wikipedia.find_shortest_path('渋谷','JR')

    top_pages = wikipedia.find_most_popular_pages()
    print(top_pages)
