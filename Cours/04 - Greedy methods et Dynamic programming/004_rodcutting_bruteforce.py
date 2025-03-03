import itertools

p = [1,5,8,9,10,17,17,20]
p = [1,2,3,3,3,4,5,5,5,7,8,10,11,14,14,15,16,16,17,18,19,20,21,23,24]
n = len(p)

# solution sans découpe
valeur_optimale = p[-1]
decoupe_optimale = [0,n]


# on teste toutes les découpes possibles
for k in range(1,n):
    for subset in itertools.combinations(range(1,n), k):
        decoupe = list(subset)
        decoupe.insert(0,0) # on ajoute 0 en début de liste
        decoupe.append(n)
        print(decoupe)
        valeur_morceau = 0
        for i in range(0, len(decoupe)-1):
            longueur_morceau = decoupe[i+1] - decoupe[i]
            valeur_morceau += p[longueur_morceau-1]
            if valeur_morceau > valeur_optimale:
                valeur_optimale = valeur_morceau
                decoupe_optimale = decoupe

print(valeur_optimale, decoupe_optimale)