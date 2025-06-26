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

## other

- dict can pop key
- set: remove() or pop(): will have key error if key not exist
- set: discard(): avoid such key error
- google docs can insert code block
-

## sketch out the code:

- This might means we keep status records like visited / used invalid paths
- What’s the size of a 5000 square matrix of integers (complete graph) in python?

  - using np can save memory(100-200MB)
  - only store half of them since it's symmetry graph(may get slower)

- Fn: find path
- Fn: refine current path
- Fn: while true, refine current path
- Fn: write current state into pkl each 1000 iterations
- Fn: write best path into output file
- Fn: find cross and resolve (swap)

  - If in current path such (ab) (cd)exists that:
  - Distance ab > ad and cd > cb: create ad, cb, remove ab , cd
  - Until there’s nothing to swap

- (potentially way to optimize:)
- Pkl (cache_a.pkl) contains:

  - Current best path
  - Matrix(if use matrix), distances calculated
  - Write each 1000times run into pkl to release memory / save results. So next time start from that result

- In common: a helper fn:
  - Read current output(aka best path into lists to continue working on it)
  - write current into output.csv for visualizer

## concepts:

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
  - detect **ccw** via vector product
    - (the result can be considered their z result)

## reference:

- [detect when to swap in 2-opt](https://en.wikipedia.org/wiki/2-opt)
- [3-opt](https://github.com/ozanyerli/tsp3opt/blob/main/tsp3opt.c)
- [3-2opt](https://www.cst.nihon-u.ac.jp/research/gakujutu/58/pdf/L-56.pdf)
- [simulated annealing](http://youtube.com/watch?v=GiDsjIBOVoA&t=989s)
- [Branch and bound](https://www.youtube.com/watch?v=1FEP_sNb62k)
- [ILS](https://en.wikipedia.org/wiki/Iterated_local_search)

## ideas:

### 2-opt, 3-opt:

for 3-opt:

- 2 tours will share at least 2 edges (0 -> 1 and n-1 -> 0)
- remove 2 edges that not share vertexes
- handle degenerate cases
- seems sensitive to float deviation(float 32 is not sufficient for square root )

### Iterated local search:

- haven't implemented

### simulated annealing:

- the params(cooling rate and initial temperature) seems significantly effect output

## others:

syntax:

- slicing and assignment.(e.g., `my_list[start_index:end_index] = my_list[start_index:end_index][::-1]`)
