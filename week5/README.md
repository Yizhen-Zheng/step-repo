## concepts:

## reference:

- [2-opt](https://en.wikipedia.org/wiki/2-opt)
- [3-opt](https://github.com/ozanyerli/tsp3opt/blob/main/tsp3opt.c)
- [3-2opt](https://www.cst.nihon-u.ac.jp/research/gakujutu/58/pdf/L-56.pdf)
- [simulated annealing](http://youtube.com/watch?v=GiDsjIBOVoA&t=989s)
- [Branch and bound](https://www.youtube.com/watch?v=1FEP_sNb62k)
- [Branch and bound](https://en.wikipedia.org/wiki/Branch_and_bound)
- [ILS](https://en.wikipedia.org/wiki/Iterated_local_search)

## ideas:

### 2-opt, 3-opt:

#### 2-opt:

- **lengthDelta:**
  = - dist(route[v1], route[v1+1]) - dist(route[v2], route[v2+1]) + dist(route[v1+1], route[v2+1]) + dist(route[v1], route[v2])
  detect if a 2-opt swap would reduce distances
- **counter clock wise:**
  more used in geometry
  resolve visual cross, faster
  direction based detection
  e.g.: (a1, a2)(b1, b2) :
  if b1 -> b2 -> a1 is same direction as b1 -> b2 -> a2, and a1 -> a2 -> b1 is same direction as a1 -> a2 -> b2, they're not corssing
  if going to another segement's vertexes from current segement's one vertex needs to diverge to 2 directions, they're crossing

  - the code used to detect **ccw** has to do with vector product
    - (the result can be considered their z result)

- while we can detect and resolve visual crosses with counter clockwise method, calculating distance delta is more efficient since it not only find literal crosses, but also those potentially better choices originally don't form visual 'cross'
- counter-clockwise more used in geometric calculation, slightly faster for avoiding calculating square

#### 3-opt:

- 2 tours will share at least 2 edges (0 -> 1 and n-1 -> 0)
- remove 2 edges that not share vertexes
- handle degenerate cases
- seems sensitive to float deviation(float 32 is not sufficient for square root )

### Iterated local search:

- haven't implemented

### simulated annealing:

- the params(cooling rate and initial temperature) seems significantly effect output
- faster than 3-opt

### genetic algorithm

[GA](https://en.wikipedia.org/wiki/Genetic_algorithm)

### Branch and Bound

- pruning: reduce the size of decision tree

- reduce a matrix:
  - use a reduce matrix to find least needed cost
- a branch will have a trie of instances(like subset/leave node)
- a DP-like subset to prevent repeated visiting
- choose a feasible child to explore furthur
- once only 1 option left, if returns the current_best_value, which will become the upper bound for exploring other branches
- by updating the upper bound, we pruning the choices
- will be killed if run N=2000 directly without memory optimization
- fast for smaller data sets

for the 1st node, there're N-1 choices(imagine a trie), at start point our initial cost is the 'least needed coast' we got from reducing

- considering recursion depth limit, we can use stack with backtrace

### for dataset with 8000 cities:

if we hold a dist_matrix of float64 of size 8000x8000, that will be about 0.5 GB, and with BranchBound we're going to copy many of this.
if split them into sub_dist_matrix, also we need to in some way keep the origin indexes in origin cities.
intuitive idea:
first make origin dist_matrix and put it into pkl, and remove from memory.
then write cities into sub*cities*[nth] csv, each row has (origin_idx, x, y).
then in a while loop, :
read these sub_cities and make their own dist_matrix,
then remove the sub*cities[nth] csv from memory, solve every of them with BB, and write it into a local_solution*[nth].csv, with local_idx,
each time after finishing writing these local*solution*[nth].csv, we remove them from memory and go to read next sub_cities input and solve it.
then finishing this while loop of solving and writing, we make the tour_array list,
for i in len(number_of_sub_solutions):
we pick up the sub*cities*[nth] csv and local*solution*[nth].csv, replace the local city idx with origin city idx, and append this solution with global idx to tour_array, and finally use the connect_nearest_neighbor to connect all?

## others:

syntax:

- slicing and assignment.(e.g., `my_list[start_index:end_index] = my_list[start_index:end_index][::-1]`)
- dict can pop key
- set: remove() or pop(): will have key error if key not exist
- set: discard(): avoid such key error
- google docs can insert code block
-

## interview technics

- confirm in / out type
  - (may be something like set, dict, arr...),
  - input size
  - edge case
  - uppercase / lowercase / alphabet / space / empty ...
- write input example
- optimization
- time / spcae complexity
- variable / func name: self explanatory
- make test case shorter
- be care of pace (about 35 min time limit)

```shellsession
python -m http.server # For Python 3
python -m SimpleHTTPServer 8000 # If you don’t want to install Python 3
```

Then, open a browser and navigate to the
[http://localhost:8000/visualizer/build/default/](http://localhost:8000/visualizer/build/default/).
