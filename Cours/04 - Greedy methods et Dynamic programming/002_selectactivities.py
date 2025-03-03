s = [1,3,0,5,3,5,6,8,8,2,12]
f = [4,5,6,7,8,9,10,11,12,13,14]

sf = list(zip(s, f))
sf.sort(key=lambda x: x[1]) #on trie suivant les dates de fin

solution = []
date_de_fin = 0

for activite in sf:
    if activite[1] > date_de_fin:
        solution.append(activite)
        date_de_fin = activite[0]

print(solution, date_de_fin)