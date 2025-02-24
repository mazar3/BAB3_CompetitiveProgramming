# 210668

import time

input_file = "f_tokyo.in"

def read_input(file_path):
    with open(file_path, 'r') as file:
        W, H = map(int, file.readline().split())
        N, M, R = map(int, file.readline().split())
        buildings = []
        for _ in range(N):
            X, Y, L, C = map(int, file.readline().split())
            buildings.append((X, Y, L, C))
        antennas = []
        for _ in range(M):
            R, C = map(int, file.readline().split())
            antennas.append((R, C))
    return W, H, N, M, R, buildings, antennas


start_time = time.time()

W, H, N, M, R, buildings, antennas = read_input(input_file)
print(f"Input lu : Grille {W}x{H}, {N} bâtiments, {M} antennes, récompense {R}")

# tri des antennes et des batiments par vitesse de connexion (décroissante)
antenna_order = sorted(range(M), key=lambda j: -antennas[j][1])
building_order = sorted(range(N), key=lambda b: -buildings[b][3])

non_covered = set(range(N))  # batiments non couverts
occupied = set()  # positions occupées
placed_antennas = []  # antennes placées : (id, x, y)
print(f"Nombre initial de bâtiments non couverts : {len(non_covered)}")

for i, ant_id in enumerate(antenna_order):
    A_R, A_C = antennas[ant_id]  # portée & vitesse

    placed = False
    for b in building_order:
        if b not in non_covered:
            continue  # le batiment est déjà couvert
        b_x, b_y = buildings[b][0], buildings[b][1]
        if (b_x, b_y) not in occupied:
            # on place l'antenne
            placed_antennas.append((ant_id, b_x, b_y))
            occupied.add((b_x, b_y))

            # on trouve les batiments couverts
            to_remove = []
            for b_prime in non_covered:
                dist = (abs(b_x - buildings[b_prime][0]) +
                        abs(b_y - buildings[b_prime][1]))
                if dist <= A_R:
                    to_remove.append(b_prime)

            # retirer les batiments déjà couverts
            for b_prime in to_remove:
                non_covered.remove(b_prime)
            placed = True
            break

    if not placed:
        print(f"Aucune position libre trouvée pour l'antenne {ant_id}")

    if (i + 1) % 100 == 0:
        print(f"Antennes traitées : {i + 1}/{M}, Bâtiments non couverts restants : {len(non_covered)}")

print(f"\nPlacement terminé. Antennes placées : {len(placed_antennas)}")
if non_covered:
    print(f"Nombre de bâtiments non couverts : {len(non_covered)}")
else:
    print("Tous les bâtiments sont couverts.")

with open(input_file[0] + "_output.txt", 'w') as output_file:
    output_file.write(f"{len(placed_antennas)}\n")
    for ant_id, x, y in placed_antennas:
        output_file.write(f"{ant_id} {x} {y}\n")
print("Fichier de sortie généré.")

end_time = time.time()
print(f"Temps total d'exécution : {end_time - start_time:.2f} secondes")