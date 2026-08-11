import heapq
import random

ROWS, COLS = 30, 60
OBSTACLE_DENSITY = 0.28
SEED = 7


def build_map(rows, cols, density, seed):
    rng = random.Random(seed)
    while True:
        grid = [["#" if rng.random() < density else "." for _ in range(cols)]
                for _ in range(rows)]
        grid[0][0] = grid[rows - 1][cols - 1] = "."
        walkable = {(r, c) for r in range(rows) for c in range(cols)
                    if grid[r][c] == "."}
        if reachable(walkable, (0, 0), (rows - 1, cols - 1)):
            return grid, walkable


def reachable(walkable, start, goal):
    seen, stack = {start}, [start]
    while stack:
        node = stack.pop()
        if node == goal:
            return True
        for nxt in neighbours(node, walkable):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return False


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbours(node, walkable):
    r, c = node
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        candidate = (r + dr, c + dc)
        if candidate in walkable:
            yield candidate


def search(walkable, start, goal, use_heuristic=True):
    h = manhattan if use_heuristic else (lambda a, b: 0)

    frontier = [(h(start, goal), 0, start)]        # (f_score, tiebreak, node)
    came_from = {start: None}
    cost_so_far = {start: 0}
    counter = expanded = 0
    visited = set()

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        expanded += 1

        if current == goal:
            path = []
            while current is not None:             
                path.append(current)
                current = came_from[current]
            return path[::-1], expanded, cost_so_far[goal], visited

        for nxt in neighbours(current, walkable):
            new_cost = cost_so_far[current] + 1
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                came_from[nxt] = current
                counter += 1
                heapq.heappush(frontier, (new_cost + h(nxt, goal), counter, nxt))

    return None, expanded, None, visited


def render(grid, path, visited, title):
    route = set(path or [])
    print(f"\n   {title}")
    for r, row in enumerate(grid):
        line = ""
        for c, ch in enumerate(row):
            pos = (r, c)
            if pos == (0, 0):
                line += "S"
            elif pos == (len(grid) - 1, len(row) - 1):
                line += "G"
            elif pos in route:
                line += "*"
            elif ch == "#":
                line += "#"
            elif pos in visited:
                line += "\u00b7"   
            else:
                line += " "
        print("   " + line)


grid, walkable = build_map(ROWS, COLS, OBSTACLE_DENSITY, SEED)
start, goal = (0, 0), (ROWS - 1, COLS - 1)

path, a_expanded, cost, a_visited = search(walkable, start, goal, True)
_, d_expanded, d_cost, d_visited = search(walkable, start, goal, False)

print("=" * 66)
print("A* PATH PLANNING  —  heuristic vs no heuristic")
print("=" * 66)

render(grid, path, a_visited, f"A* — explored {a_expanded} nodes")
render(grid, path, d_visited, f"Dijkstra — explored {d_expanded} nodes")

print(f"\n   optimal path cost : A* {cost} steps | Dijkstra {d_cost} steps -> identical")
print(f"   A* expanded       : {a_expanded}  ({a_expanded/len(walkable):.0%} of the map)")
print(f"   Dijkstra expanded : {d_expanded}  ({d_expanded/len(walkable):.0%} of the map)")
print(f"\n   heuristic saved   : {d_expanded - a_expanded} expansions"
      f"  ({1 - a_expanded/d_expanded:.0%} less work for the same answer)")