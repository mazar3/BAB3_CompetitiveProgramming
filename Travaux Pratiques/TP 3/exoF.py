n = int(input())
d_i = list(map(int, input().split()))
e_i = list(map(int, input().split()))

exercices = list(zip(d_i, e_i))

valides = []
non_valides = []
for d, e in exercices:
    if d > e:
        non_valides.append((d, e))
    else:
        valides.append((d, e))

valides.sort(key=lambda x: x[1])
exercices_result = valides + non_valides

cumulative = 0
retards = 0
for d, e in exercices_result:
    cumulative += d
    if cumulative > e:
        retards += 1

print(retards)