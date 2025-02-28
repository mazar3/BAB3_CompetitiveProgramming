import time

def somme_sous_sequence_max_divide_conquer(v, debut, fin):
    # on divise en deux moitiés
    milieu = (debut + fin) // 2

    # cas 1 : si la sous-séquence est entièrement à gauche
    gauche_somme, gauche_debut, gauche_fin = somme_sous_sequence_max_divide_conquer(v, debut, milieu)

    # cas 2 : si la sous-séquence entièrement est à droite
    droite_somme, droite_debut, droite_fin = somme_sous_sequence_max_divide_conquer(v, milieu + 1, fin)

    # cas 3 : si la sous-séquence passe par le milieu
    # on va alors calculer et additionner la partie de gauche et droite

    # partie de gauche (on calcule la somme max allant du début vers le milieu)
    gauche_somme_max = float('-inf')
    somme = 0
    gauche_index = milieu
    for i in range(milieu, debut - 1, -1):
        somme += v[i]
        if somme > gauche_somme_max:
            gauche_somme_max = somme
            gauche_index = i

    # partie de droite (on calcule la somme max allant du milieu vers la fin)
    droite_somme_max = float('-inf')
    somme = 0
    droite_index = milieu + 1
    for i in range(milieu + 1, fin + 1):
        somme += v[i]
        if somme > droite_somme_max:
            droite_somme_max = somme
            droite_index = i

    # somme totale traversant le milieu
    milieu_somme = gauche_somme_max + droite_somme_max

    # on compare les trois cas et on return le meilleur
    if gauche_somme >= droite_somme and gauche_somme >= milieu_somme:
        return gauche_somme, gauche_debut, gauche_fin
    elif droite_somme >= gauche_somme and droite_somme >= milieu_somme:
        return droite_somme, droite_debut, droite_fin
    else:
        return milieu_somme, gauche_index, droite_index


# test avec le tableau de l'exercice brute force
# sortie attendue : "DebutOPT: 7, FinOPT: 10, somme_max: 43"
v_test = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
start_time = time.time()
somme_max, debut_opt, fin_opt = somme_sous_sequence_max_divide_conquer(v_test, 0, len(v_test) - 1)
print(f"> Petit tableau (test) :")
print(f"   > Sous séquence de somme maximale trouvée :")
print(f"      > Position : {debut_opt}->{fin_opt}")
print(f"      > Somme : {somme_max}")
print(f"      > Temps d'exécution : {time.time() - start_time:.4f} seconds")

# application au grand tableau dans "tres_long_vecteur.txt"
try:
    with open("tres_long_vecteur_pour_soussequencedesommemax.txt", "r") as f:
        v = list(map(int, f.readline().split()))

    start_time = time.time()
    somme_max, debut_opt, fin_opt = somme_sous_sequence_max_divide_conquer(v, 0, len(v) - 1)
    print(f"\n> Grand tableau (le fichier txt) :")
    print(f"   > Sous séquence de somme maximale trouvée :")
    print(f"      > Position : {debut_opt}->{fin_opt}")
    print(f"      > Somme : {somme_max}")
    print(f"      > Temps d'exécution : {time.time() - start_time:.4f} seconds")
except FileNotFoundError:
    print("\nErreur : Le fichier txt n'a pas été trouvé")