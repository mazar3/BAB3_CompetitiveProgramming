def knapsack_progdyn(w, v, W):
    n = len(w) # nombres d'objet
    f = [[0 for i in range(W+1)] for _ in range(n+1)]

    # on remplit le tableau f de gauche à droite, de haut en bas
    for k in range(1, n+1):
        for j in range(1, W+1):
            if w[k-1] <= j and v[k-1] + f[k-1][j-w[k-1]] > f[k-1][j]:
                f[k][j] = v[k-1] + f[k-1][j-w[k-1]]
            else:
                f[k][j] = f[k-1][j]
    return f

w = [1,2,5,6,7]
v = [1,6,18,22,28]
W = 11
f = knapsack_progdyn(w,v,W)

print(f)