def est_carre(grille, n):
    coins_noirs = [(i, j) for i in range(n) for j in range(n) if grille[i][j] == '#']
    if not coins_noirs:
        return "NO"

    x_min, y_min = min(coins_noirs)
    x_max, y_max = max(coins_noirs)
    if x_max - x_min != y_max - y_min:
        return "NO"

    for i in range(x_min, x_max + 1):
        for j in range(y_min, y_max + 1):
            if grille[i][j] != '#':
                return "NO"

    return "YES"

n = int(input())
grille = [input().strip() for _ in range(n)]
print(est_carre(grille, n))
