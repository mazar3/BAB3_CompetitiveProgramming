p = [0,1,5,8,9,10,17,17,20]
#p = [0,1,2,3,3,3,4,5,5,5,7,8,10,11,14,14,15,16,16,17,18,19,20,21,23,24]

n = len(p)-1 #n est le nombre de centimetres de la tige

# on stocke peu à peu les solutions optimales des sous problèmes
f = [0 for i in range(n+1)]

for i in range(1,n+1):
    fmax = 0
    for j in range(1,i+1):
        valeur = p[j] + f[i-j]
        if valeur > fmax:
            fmax = valeur
    f[i] = fmax

print(f)
print(f"La solution otpimale du problème = {f[-1]}")