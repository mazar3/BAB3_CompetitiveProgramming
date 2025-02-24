import itertools
billets = [50, 20, 10, 5, 1]

S = 100

possibilites = set()

for k in range(1, S+1):
    for subset in itertools.combinations_with_replacement(billets, k):
        if sum(subset) == S:
            possibilites.add(tuple(subset))
            print(f'Mon tour {k} -> {subset}')
print(len(possibilites))