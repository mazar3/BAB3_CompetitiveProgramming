#somme a rendre
S = 93

#les types de billets disponibles
billets = [1, 2, 5, 10, 20, 50, 100, 500, 1000] 

solution = []

for billet in sorted(billets, reverse=True):
    while billet <= S:
        S -= billet
        solution.append(billet)

print(solution)