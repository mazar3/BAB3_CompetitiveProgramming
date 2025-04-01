import heapq


def dijkstra(graph, start, end):
    """
    Trouve le plus court chemin de start à end en utilisant l'algorithme de Dijkstra.

    Args:
        graph (dict): Graphe sous forme de liste d'adjacence pondérée
        start (int): Nœud de départ
        end (int): Nœud d'arrivée

    Returns:
        int: Longueur du plus court chemin
    """
    # File de priorité pour stocker les couples (distance, nœud)
    pq = [(0, start)]
    # Dictionnaire des distances minimales depuis le départ
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        # Si on a déjà trouvé un chemin plus court vers ce nœud, on l'ignore
        if current_distance > distances[current_node]:
            continue

        # Parcours de tous les voisins du nœud courant
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            # Si on a trouvé un chemin plus court vers le voisin, on met à jour
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances[end]


n, m = map(int, input().split())

graph = {i: [] for i in range(1, n + 1)}
for _ in range(m):
    u, v, w = map(int, input().split())
    graph[u].append((v, w))
    graph[v].append((u, w))

shortest_path_length = dijkstra(graph, 1, n)

print(shortest_path_length)