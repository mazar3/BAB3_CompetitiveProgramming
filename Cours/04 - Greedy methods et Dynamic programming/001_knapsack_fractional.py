#poids
w = [3, 2, 1, 4, 5]

#valeurs
v = [25, 20, 15, 40, 50] 

#contenance du sac-à-dos
W = 6

ratios = [vi/wi for vi, wi in zip(v, w)]
x = [0 for i in v] #variables du problème

somme_wi = 0
somme_vi = 0

while True:
    imax = ratios.index(max(ratios))
    x[imax] = min(1,(W - somme_wi)/w[imax])
    somme_wi += w[imax]*x[imax]
    somme_vi += v[imax]*x[imax]
    ratios[imax] = 0
    if somme_wi >= W:
        break

print(x, somme_vi, somme_wi)