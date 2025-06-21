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

- Write each 100times run into pkl to release memory / save results. So next time start from that result
- This might means we keep status records like visited / used invalid paths
- What’s the size of a 5000 square matrix of integers (complete graph) in python?

  - using np can save memory
  - only store half of them since it's symmetry graph

- No need for class at this point .
- Fn: find path
- Fn: refine current path
- Fn: while true, refine current path
- Fn: write current state into pkl each 1000 iterations
- Fn: write best path into output file
- Fn: find cross and resolve (swap)
  - If in current path such (ab) (cd)exists that:
  - Distance ab > ad and cd > cb: create ad, cb, remove ab , cd
  - Until there’s nothing to swap
- Pkl (cache_a.pkl) contains:
  - Current best path
  - Matrix(if use matrix), distances calculated
- In common: a helper fn:
  - Read current output(aka best path into lists to continue working on it)
  - write current into output.csv for visualizer
