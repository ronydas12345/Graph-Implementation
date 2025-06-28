import os

class Graph:
    def __init__(self, d: dict):
        self.graph = d
    def append(self, node, lst):
        self.graph[node] = lst
    def dfs(self, node): # convert to stack
        res = []
        def search(node, visited):
            visited.add(node)
            res.append(node)
            for vertex in self.graph[node]:
                if vertex not in visited:
                    search(vertex, visited)
        
        search(node, set())
        return res
    
    def bfs(self, node):
        res, visited, queue = [], set(node), [node]
        while queue:
            node = queue.pop(0)
            for vertex in self.graph[node]:
                if vertex not in visited:
                    visited.add(vertex)
                    queue.append(vertex)
            res.append(node)
        return res
    
    def get_components(self):
        visited, components = [], []
        for vertex in self.graph:
            if vertex not in visited:
                path = self.dfs(vertex)
                visited.extend(path)
                components.append(path)

        return components

class AntiCycleSet:
    def __init__(self):
        self.parent = {}
    
    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]
    
    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b: return False
        self.parent[root_b] = root_a
        return True

class Iterator:
    def __init__(self, start, end):
        self.curr = start
        self.end = end

    def get(self):
        return self
    
    def next(self):
        if self.curr > self.end:
            return False
        else:
            self.curr += 1
            return self.curr - 1


class DistGraph(Graph):
    def dfs(self, node):
        res = []
        def search(node, visited):
            visited.add(node)
            res.append(node)
            for neighbor, _ in self.graph[node]:
                if neighbor not in visited:
                    search(neighbor, visited)
        search(node, set())
        return res

    def bfs(self, node):
        res, visited, queue = [], set(node), [node]
        while queue:
            node = queue.pop(0)
            for neighbor, _ in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
            res.append(node)
        return res

    def set_dist(self, a, b, val):
        for i, (neighbor, _) in enumerate(self.graph[a]):
            if neighbor == b:
                self.graph[a][i] = (neighbor, val)
                break
        for i, (neighbor, _) in enumerate(self.graph[b]):
            if neighbor == a:
                self.graph[b][i] = (neighbor, val)
                break

    def get_edges(self):
        visited, edges = set(), []
        for i in self.graph:
            for a, b in self.graph[i]:
                if (a, i) not in visited:
                    edges.append((b, i, a))
                    visited.add((i, a))
        return edges
    
    def kruskal(self):
        anticycle = AntiCycleSet()
        for node in self.graph:
            anticycle.parent[node] = node
        
        edges = self.get_edges()
        edges.sort()

        mst = []
        for dist, a, b in edges:
            if anticycle.union(a, b):
                mst.append((a, b, dist))
        return mst
    """
    def prim(self):
        edges, visited, mst = self.get_edges(), set(), []
        edges.sort()

        candidates = set()
        u, v, w = edges[0][2], edges[0][1], edges[0][0]
        for i in range(len(self.graph) - 1):
            visited.add(u)
            visited.add(v)

            mst.append((u, v, w))

            for neighbor in self.graph[u]:
                if neighbor[0] not in visited and (neighbor[1], u, neighbor[0]) not in candidates:
                    candidates.add((neighbor[1], u, neighbor[0]))
            
            for neighbor in self.graph[v]:
                if neighbor[0] not in visited and (neighbor[1], v, neighbor[0]) not in candidates:
                    candidates.add((neighbor[1], v, neighbor[0]))
            
            w, u, v = sorted(candidates)[0]
            candidates.remove((w, u, v))
        
        return mst
    """
    def prim(self):
        start = next(iter(self.graph))
        visited, mst, edges = [start], [], []

        for neighbor, weight in self.graph[start]:
            edges.append((weight, start, neighbor))
        
        while len(visited) < len(self.graph):
            min_index, it = 0, Iterator(1, len(edges) - 1).get()
            i = it.next()
            while i is not False:
                if edges[i][0] < edges[min_index][0]:
                    min_index = i
                i = it.next()
            
            weight, u, v = edges.pop(min_index)
            if v in visited: continue
            visited.append(v)
            mst.append((u, v, weight))

            it = Iterator(0, len(self.graph[v]) - 1).get()
            i = it.next()
            while i is not False:
                neighbor, w = self.graph[v][i]
                if neighbor not in visited:
                    edges.append((w, v, neighbor))
                
                i = it.next()
            
        return mst

    def dijkstra(self, source):
        dist, parent, visited, size, curr = self.graph.fromkeys(self.graph.keys(), float("inf")), self.graph.fromkeys(self.graph.keys(), None), set(), len(self.graph), source
        visited.add(source)

        dist[source] = 0
        for vert in range(size):
            for neighbor in self.graph[curr]:
                if neighbor[0] not in visited and dist[curr] + neighbor[1] < dist[neighbor[0]]:
                    dist[neighbor[0]] = dist[curr] + neighbor[1]
                    parent[neighbor[0]] = curr
                
            min_dist, next_vert = float("inf"), None
            for v, d in dist.items():
                if d < min_dist and v not in visited:
                    min_dist = d
                    next_vert = v
            
            if next_vert is not None:
                curr = next_vert
                visited.add(curr)

        return dist, parent

g = {
    "a": ["b", "e"],
    "b": ["a", "c", "g"],
    "c": ["b", "d"],
    "d": ["c", "f"],
    "e": ["a", "g", "f"],
    "f": ["e", "d"],
    "g": ["b", "e"]
}

graph = Graph(g)
print(graph.dfs("a"))
print(graph.bfs("a"))
print(graph.get_components())

print("-" * 37)
#----------------------------

g1 = {
    "a": [("b", 3), ("e", 2)],
    "b": [("a", 3), ("c", 4), ("g", 6)],
    "c": [("b", 4), ("d", 5)],
    "d": [("c", 5), ("f", 2)],
    "e": [("a", 2), ("g", 7), ("f", 1)],
    "f": [("e", 1), ("d", 2)],
    "g": [("b", 6), ("e", 7)]
}

dist_graph = DistGraph(g1)
print(dist_graph.dfs("a"))
print(dist_graph.bfs("a"))
print(dist_graph.get_components())
print(dist_graph.kruskal())
print(dist_graph.prim())
#----------------------------

print("-" * 37)
g2 = {
    "a": [("b", 28), ("f", 10)],
    "b": [("a", 28), ("g", 14), ("c", 16)],
    "c": [("b", 16), ("d", 12)],
    "d": [("c", 12), ("e", 22), ("g", 18)],
    "e": [("d", 22), ("f", 25), ("g", 24)],
    "f": [("a", 10), ("e", 25)],
    "g": [("b", 14), ("d", 18), ("e", 24)]
}
dist_graph2 = DistGraph(g2)
print(dist_graph2.dfs("a"))
print(dist_graph2.bfs("a"))
print(dist_graph2.get_components())
print(dist_graph2.prim())
print(dist_graph2.dijkstra("a"))

input()
os.system("cls")

class GraphInterface:
    def __init__(self, graph):
        self.graph = graph

    def menu(self):
        while True:
            print("\n--- Graph Menu ---")
            print("  [1] Display Graph")
            print("  [2] Add Edge")
            print("  [3] Update Distance")
            print("  [4] Find Path using Dijkstra")
            print("  [5] Kruskal's MST")
            print("  [6] Prim's MST")
            print("  [7] DFS Traversal")
            print("  [8] BFS Traversal")
            print("  [9] Exit")
            print("  [10] Clear")
            choice = input("Enter your choice: ")

            if choice == "1":
                for node in self.graph.graph:
                    print(node, "->", self.graph.graph[node])
            elif choice == "2":
                a = input("Enter first node: ")
                b = input("Enter second node: ")
                w = int(input("Enter weight: "))
                if a not in self.graph.graph:
                    self.graph.graph[a] = []
                if b not in self.graph.graph:
                    self.graph.graph[b] = []
                self.graph.graph[a].append((b, w))
                self.graph.graph[b].append((a, w))
                print("Edge added.")
            elif choice == "3":
                a = input("Enter first node: ")
                b = input("Enter second node: ")
                w = int(input("Enter new weight: "))
                self.graph.set_dist(a, b, w)
                print("Distance updated.")
            elif choice == "4":
                source = input("Enter source node: ")
                dist, parent = self.graph.dijkstra(source)
                print("Distances:", dist)
                print("Parents:", parent)
            elif choice == "5":
                print("Kruskal MST:", self.graph.kruskal())
            elif choice == "6":
                print("Prim MST:", self.graph.prim())
            elif choice == "7":
                start = input("Enter start node for DFS: ")
                print("DFS Traversal:", self.graph.dfs(start))
            elif choice == "8":
                start = input("Enter start node for BFS: ")
                print("BFS Traversal:", self.graph.bfs(start))
            elif choice == "9":
                print("Exiting.")
                break
            elif choice == "10":
                os.system("cls")
            else:
                print("Invalid choice.")


menu = GraphInterface(DistGraph(dist_graph).graph)

menu.menu()