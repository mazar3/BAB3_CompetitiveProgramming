def rodcutting(p,n):
    ...

p = [0,1,5,8,9,10,17,17,20]
#p = [0,1,2,3,3,3,4,5,5,5,7,8,10,11,14,14,15,16,16,17,18,19,20,21,23,24]

#n est le nombre de centimetres de la tige
n = len(p) - 1

def rodcutting_optimal(p, n):
    if n == 0:
        return 0
    fmax = p[n]
    for j in range(1,n):
        f_moins_j = rodcutting_optimal(p, n-j)
        valeur = p[j] + f_moins_j
        if valeur > fmax:
            fmax = valeur
    return fmax

print(f"Valeur max = {rodcutting_optimal(p,n)}")