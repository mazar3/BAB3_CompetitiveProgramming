from collections import deque

def solve_maze():
    # Lecture des dimensions de la grille
    n, m = map(int, input().split())

    # Lecture de la grille
    grid = []
    start = None
    for i in range(n):
        row = input()
        grid.append(row)
        # Trouver la position de départ (K)
        if "K" in row and start is None:
            start = (i, row.index("K"))

    # Directions possibles: haut, bas, gauche, droite
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # BFS pour trouver un chemin
    queue = deque([start])
    visited = set([start])

    while queue:
        x, y = queue.popleft()

        # Explorer les voisins
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Vérifier que la position est valide
            if 0 <= nx < n and 0 <= ny < m and (nx, ny) not in visited:
                # Si on trouve l'arrêt de bus
                if grid[nx][ny] == "B":
                    return "yes"
                # Si c'est un emplacement libre
                if grid[nx][ny] == ".":
                    queue.append((nx, ny))
                    visited.add((nx, ny))

    # Si on n'a pas trouvé de chemin
    return "no"


print(solve_maze())
