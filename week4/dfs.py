#! /usr/bin/python3
import collections


# An example graph structure
links = {"A": ["B", "E", "G"],
         "B": ["C"],
         "C": ["D"],
         "D": ["E"],
         "E": ["B", "F"],
         "F": [],
         "G": ["F"]}


# A helper function to find a path.
def find_path(goal, previous):
    path = []
    node = goal
    path.append(node)
    while previous[node]:
        node = previous[node]
        path.append(node)
    path.reverse()
    return path


# dfs_with_recursion finds A -> B -> C -> D -> E -> F first.
def dfs_with_recursion(start, goal):
    print("dfs_with_recursion:")
    visited = {}
    previous = {}

    visited[start] = True
    previous[start] = None
    recursion(start, goal, visited, previous)

    if goal in previous:
        print(" -> ".join(find_path(goal, previous)))
    else:
        print("Not found")


def recursion(node, goal, visited, previous):
    if node == goal:
        return True
    for child in links[node]:
        if not child in visited:
            visited[child] = True
            previous[child] = node
            if recursion(child, goal, visited, previous):
                return True
    return False


# dfs_with_stack finds A -> G -> F first.
def dfs_with_stack(start, goal):
    print("dfs_with_stack:")
    stack = collections.deque()
    visited = {}
    previous = {}

    stack.append(start)
    visited[start] = True
    previous[start] = None
    while len(stack):
        node = stack.pop()
        if node == goal:
            break
        for child in links[node]:
            if not child in visited:
                stack.append(child)
                visited[child] = True
                previous[child] = node

    if goal in previous:
        print(" -> ".join(find_path(goal, previous)))
    else:
        print("Not found")


# Challenge quiz: Implement DFS using a stack that visits nodes and edges
# in the same order as dfs_with_recursion. In other words, implement DFS that
# finds A -> B -> C -> D -> E -> F first using a stack.

def dfs_with_stack_in_the_recursion_order(start, goal):
    '''over complexified version'''
    print("dfs_with_stack_in_the_recursion_order:")
    stack = collections.deque()
    visited = {start}
    previous = {}
    stack.append(collections.deque(start))
    previous[start] = None

    found = False
    prev_memo = None
    while stack and not found:
        current_q = stack[-1]
        # if find=True: compare path
        while current_q:
            node = current_q.popleft()
            previous[node] = prev_memo
            prev_memo = node
            if node == goal:
                found = True
                break
            new_q = collections.deque()
            for child in links[node]:
                if child not in visited:
                    new_q.append(child)
                    visited.add(child)
            stack.append(new_q)
            current_q = stack[-1]
        stack.pop()
    print(previous)

    if goal in previous:
        print(" -> ".join(find_path(goal, previous)))
    else:
        print("Not found")


def dfs_with_stack_in_the_recursion_order2(start, goal):
    '''optimized version'''
    print("dfs_with_stack_in_the_recursion_order without nested double end queue:")
    # (node,path)
    stack = [(start, [start])]
    visited = {start}
    previous = {}
    previous[start] = None

    path_found = []
    while stack:
        (current_node, path) = stack.pop()
        print(current_node)
        visited.add(current_node)
        if current_node == goal:
            path_found = path
            break
        for neighbor in reversed(links.get(current_node, [])):
            if neighbor not in visited:
                new_path = path[:]
                new_path.append(neighbor)
                stack.append((neighbor, new_path))
                previous[neighbor] = current_node

    print(" -> ".join(find_path(goal, previous)))
    if goal in path_found:
        print('goal found')
    else:
        print('not found')
    return


dfs_with_recursion("A", "F")
dfs_with_stack("A", "F")
dfs_with_stack_in_the_recursion_order("A", "F")
dfs_with_stack_in_the_recursion_order2("A", "F")
