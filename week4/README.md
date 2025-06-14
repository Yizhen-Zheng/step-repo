# lecture content

data structure -- graph
weighted vs unweighted
directed vs undirected graph
connected vs unconnected
strongly connected vs weakly connected
complete graph: E = N(N-1)/2

- adjacency list: O(N+E)
- adj matrix: O(N^2)

### how to know if 2 nodes are connected?:

- breadth first: queue(useful for shortest path)
- deepth first: stack(when to mark as visited: when push(most time preferred) or when pop )
  - with recuresion:
    > if dfs(child)=='found': return found
- Dijkstra's algorithm

### page rank

- random surfer model

# homework

---

to run the python file, please download the following file:
[wikipedia_dataset.zip](https://drive.google.com/file/d/1mNkmAK70JlExll9kEEHQWR08bbutce2x/view)
unzip it, and move the unzipped folder under ./week4

---

1: implement find shortest path from one page to another
2: impelment find most popular page(Page Rank), calculate top 10 pages
3: impelement find longest path without repeated pages (NP-hard)(hint: find order of traverse)

### find shortest path

- I first considered use a adjacency matrix, and realized it's impossible
  - Memory requirement (PBs of memory)
  - inefficiency for sparse dataset
  - matrix operations at large scale is costy

### find most popular page (page rank)

- use a local DB
- use adj list iteratively
- External memory algorithms
- block wise proccessing

**key learned**

#### adj matrix vs list:

- when link density > 50%
- frequent edge loopkups (matrix: O(1), list: O(E))
- matrix based algorithms: Random walk, Floyd Warshall, Graph clustering, Page Rank...
- mathematical operations (graph powers, linear algebra related analysing)
- vector related operations

### find longest path without visiting the same page twice

- NP hard:
  - non deterministic algorithms vs deterministic. P is a subset of NP
  - P: deterministic, taking polinomial(+-\*/^, finite terms) time
  - NP: non deterministic, taking polinomial time
    idea:
  - relate unsolved problem to NP hard ones, throught **reduction**
  - then if we can write non deterministic algorithm, the NP hard becomes NP complete
- clique decision problem: does a size n clique exist in a graph?
- clique optimization problem: what's the maximum size clique in a graph?

#### 1: divide into smaller cluster

- find strongly connected nodes / clusters
- remove dead ends
- connect clusters latter

#### 2: search from start and destination page (2 head)

#### 3: store pages into a DB, and divide the tasks

---

###### others:

bitwise operation in py:
AND, OR: &, |
NOT: ~
^: XOR
`>>, <<`: right, left shift

i'm trying to solve finding longest (not visit same page twice) path between 2 pages in a graph. the dataset for the graph is all japanese pages in wiki, initially represented in adj lists. so i'm thinking
