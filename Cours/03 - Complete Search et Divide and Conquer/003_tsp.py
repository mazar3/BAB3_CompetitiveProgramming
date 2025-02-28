import itertools


def bruteforceTSP(matadj, s):
    # s est la ville de départ et d'arrivée
    n = len(matadj[0]) # nombre de villes

    villes = [i for i in range(n) if i!=s]

    cout_max = float('inf')
    touropt = []
    for subset in itertools.permutations(villes):
        print(subset)
        cout_tour = matadj[s][subset[0]] # distance de s jusqu'à la première ville
        for i in range(len(subset)-1):
            cout_tour += matadj[subset[i]][subset[i+1]]
        cout_tour += matadj[subset[-1]][s]
        print(f'Mon tour {s} -> {subset} = {cout_tour}')
        if cout_tour < cout_max:
            cout_max = cout_tour
            touropt = subset
        return cout_max, touropt
 
   
    
matadj = [[0, 2, 8, 5],
         [2, 0, 3, 4],
         [8, 3, 0, 7],
         [5, 4, 7, 0]]
s = 0
cout, tour = bruteforceTSP(matadj, s)
print(f"Le tour {tour} est optimal de longueur {cout}")