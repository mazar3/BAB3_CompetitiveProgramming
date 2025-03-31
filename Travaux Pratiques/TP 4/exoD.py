# Lecture de la première ligne contenant n et r
n, r = map(int, input().split())

# Construction du graphe
graph = [[] for _ in range(n)]
for _ in range(r):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

visited = [False] * n
components = 0

# Définition du DFS récursif
def dfs(node):
    visited[node] = True
    for neighbor in graph[node]:
        if not visited[neighbor]:
            dfs(neighbor)

# Recherche des composantes connexes
for node in range(n):
    if not visited[node]:
        components += 1
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor)

# Calcul et affichage du résultat
print(components - 1)
