from collections import deque

def build_graph(size, routes):
    graph = {str(i): [] for i in range(size)}
    for route in routes:
        if len(route) >= 2:
            u, v = str(route[0]), str(route[1])
            graph.setdefault(u, []).append(v)
            graph.setdefault(v, []).append(u)  # Supprimer si graphe orienté

    return graph

def bfs_calculate_distances(graph, start):
    start = str(start)
    distances = {node: -1 for node in graph}
    distances[start] = 0
    queue = deque([start])

    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if distances[neighbor] == -1:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    return distances

def calculate_expected_time(graph, start, arrival, probas):
    if start is not None:   start = str(start)
    if arrival is not None: arrival = str(arrival)
    probas = {str(k): v for k, v in enumerate(probas, 1)}
    expected_time = 0

    if start is not None and arrival is None:
        distances = bfs_calculate_distances(graph, start)
        for node, prob in probas.items():
            if prob > 0 and node in distances:
                expected_time += prob * distances[node]

    elif start is None and arrival is not None:
        for node, prob in probas.items():
            if prob > 0:
                distances = bfs_calculate_distances(graph, node)
                if arrival in distances:
                    expected_time += prob * distances[arrival]

    elif start is not None and arrival is not None:
        distances = bfs_calculate_distances(graph, start)
        expected_time = distances.get(arrival, -1)

    else:
        raise ValueError("Au moins un des paramètres start ou arrival doit être spécifié.")

    return expected_time


n, m = map(int, input().split())
probas = list(map(float, input().split()))
routes = [input().split() for _ in range(m)]

graph = build_graph(n, routes)
print(f"{calculate_expected_time(graph, 1, None, probas) + calculate_expected_time(graph, None, n, probas):.6f}")