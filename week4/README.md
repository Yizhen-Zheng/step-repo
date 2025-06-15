# lecture content

data structure -- graph
weighted vs unweighted
directed vs undirected graph
connected vs unconnected
strongly connected vs weakly connected
complete graph: E = N(N-1)/2 for undirected, N(N-1) for directed

- adjacency list: O(N+E) good for sparse graph
- adj matrix: O(N^2), good for dense graph

### how to know if 2 nodes are connected?:

- breadth first: queue(useful for shortest path)
- deepth first: stack(when to mark as visited: when push(most time preferred) or when pop )
  - with recuresion:
    > if dfs(child)=='found': return found
- Dijkstra's algorithm

### page rank

- random surfer model

# homework

1: implement find shortest path from one page to another
2: impelment find most popular page(Page Rank), calculate top 10 pages
3: impelement find longest path without repeated pages (NP-hard)(hint: find order of traverse)

challenge quiz: implement DFS, that traverse nodes like recursion

---

to run the python file, please download the following file:
[wikipedia_dataset.zip](https://drive.google.com/file/d/1mNkmAK70JlExll9kEEHQWR08bbutce2x/view)
unzip it, and move the unzipped folder under `./week4`

**file structure:**

```
week4/
├── wikipedia_dataset/
│   ├── pages_small.txt
│   ├── links_small.txt
│   ├── pages_medium.txt
│   ├── links_medium.txt
│   ├── pages_large.txt
│   └── links_large.txt
├── wikipedia_1.py          # shortest path, pageRank
├── test_wiki_1.py          # tests for wikipedia_1.py
├── wikipedia_2.py          # longest path (partial implementation)
└── test_wiki_2.py          # tests for wikipedia_2.py
|__ dfs.py                  # a challenge quiz
```

run example:

```bash
cd ./week4
python3 wikipedia_1.py
python3 wikipedia_2.py
# enter: 'small', 'medium', or 'large'

# To run tests:
python3 test_wiki_1.py
python3 test_wiki_2.py
```

---

### find shortest path

- I first considered use a adjacency matrix. why it's impossible:
  - Memory requirement (PBs of memory)
  - inefficiency for sparse dataset
  - matrix operations at large scale is costy

### find most popular page (page rank)

- used adj list iteratively

potential ways to make it faster / more memory efficient

- change language
- matrix operations(if possible)

potential ways when ram space is not enough

- use a local DB
- External memory algorithms(disk based)
- block wise proccessing

**key learned**

#### adj matrix vs list:

adj matrix:

- when link density > 50%
- frequent edge loopkups (matrix: O(1), list: O(E))
- matrix based algorithms: Random walk, Floyd Warshall, Graph clustering, Page Rank...
- mathematical operations (graph powers, linear algebra related analysing)
- vector related operations

adj listL

- when sparse graphs
- memory efficiency
- simple traverse(BFS, DFS)

### find longest path without visiting the same page twice

- concepts surrond 'NP hard':
  - non deterministic algorithms vs deterministic. P is a subset of NP
  - P: deterministic, taking polinomial(+-\*/^, finite terms) time
  - NP: non deterministic, taking polinomial time
    idea:
  - relate unsolved problem to NP hard ones, throught reduction
  - then if we can write non deterministic algorithm, the NP hard becomes NP complete
- clique decision problem: does a size n clique exist in a graph?
- clique optimization problem: what's the maximum size clique in a graph?

---

- intuitive for find longest path (doesn't help much):
  remove dead end pages.
  only work with pages that satisfy:
  - can be accessed from start
  - can access goal
- after doing dfs.py, i'm thinking about it's seems crucial to traverse with a DFS with recursive like behaviour. in that way we can avoid 1000 recursion depth limit, and keep each path and visited independent

#### 1: divide into smaller cluster

- find strongly connected nodes / clusters
- find ways in these clusters
- connect clusters latter

#### 2: search from both start and goal page (2 head)

- meet in the middle
- not sure if this usefule, it seems similar to idea 1

#### 3: store pages into a DB, and divide the tasks

- partition problem across multiple processes (currently, iterate 1000 time in medium takes 10s seconds)
- we start with a way from start to goal.
- for each node on the path, we try to extent it to the goal, see if we can form a path
- if so, we store the path and score it
- next time we choose the path with higher score and repeat above

---

#### others:

##### bitwise operation in py:

can be used in lists and sets (e.g.: [A,B,C]&[A]: [A])
AND, OR: &, |
NOT: ~
^: XOR
`>>, <<`: right, left shift

dict.get(key, default_value)
mylist[:]: a common way to shallow copy list, which means:

- immutable elements will be deep copied
- mutable elements (nested obj) will be shallow copied

deepcopy: use copy.deepcopy

```python
  origin=[[1,2],[3,4]]
  copied=origin[:]
  origin[0][0]=0
  print(copied)#[[0,2],[3,4]]
```

iter: - my_iter=iter(iterable) returns an iterator obj - next(my_iter) - StopIteration when no more values
