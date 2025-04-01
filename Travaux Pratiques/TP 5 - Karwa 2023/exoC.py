def has_eulerian_circuit(graph, start):
    # Vérifier si tous les sommets ont un degré pair
    for vertex in graph:
        if len(graph[vertex]) % 2 != 0:
            return False

    visited = set()

    def dfs(vertex):
        visited.add(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                dfs(neighbor)

    dfs(start)

    for vertex in graph:
        if len(graph[vertex]) > 0 and vertex not in visited:
            return False

    return True

def solve_circuit_confort():
    n = int(input().strip())
    start = input().strip()

    graph = {}

    for _ in range(n):
        line = input().strip()
        gare1, gare2 = line.split()

        if gare1 not in graph:
            graph[gare1] = []
        if gare2 not in graph:
            graph[gare2] = []

        graph[gare1].append(gare2)
        graph[gare2].append(gare1)

    if has_eulerian_circuit(graph, start):
        return "ok"
    else:
        return "impossible"

print(solve_circuit_confort())
