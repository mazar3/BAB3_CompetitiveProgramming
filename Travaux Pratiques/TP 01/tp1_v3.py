# 210668

import time
from scipy.spatial import KDTree

input_file = "b_mumbai.in"

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

def place_antennas(W, H, N, M, R, buildings, antennas):
    # trier les antennes par portée décroissante
    antenna_order = sorted(range(M), key=lambda i: -antennas[i][0])

    # créer un kd-tree avec les positions des batiments
    building_positions = [(b[0], b[1]) for b in buildings]
    kd_tree = KDTree(building_positions)

    non_covered = set(range(N))
    occupied = set()
    placed_antennas = []

    for ant_id in antenna_order:
        A_R, A_C = antennas[ant_id]  # portée & vitesse
        best_coverage = 0
        best_position = None

        # positions des bâtiments non couverts
        candidate_positions = [(buildings[b_idx][0], buildings[b_idx][1]) for b_idx in non_covered if (buildings[b_idx][0], buildings[b_idx][1]) not in occupied]

        for pos in candidate_positions:
            x, y = pos
            # calculer la couverture avec un kd-tree
            indices = kd_tree.query_ball_point((x, y), A_R, p=1)
            coverage = sum(1 for idx in indices if idx in non_covered)

            if coverage > best_coverage:
                best_coverage = coverage
                best_position = (x, y)

        if best_position:
            x, y = best_position
            placed_antennas.append((ant_id, x, y))
            occupied.add((x, y))

            # mettre à jour les batiments couverts
            indices = kd_tree.query_ball_point((x, y), A_R, p=1)
            covered = [idx for idx in indices if idx in non_covered]
            for idx in covered:
                non_covered.remove(idx)

        if len(placed_antennas) % 100 == 0 or len(placed_antennas) == M:
            print(f"Antennes traitées : {len(placed_antennas)}/{M}, Bâtiments non couverts restants : {len(non_covered)}")

    return placed_antennas, len(non_covered)

start_time = time.time()
W, H, N, M, R, buildings, antennas = read_input(input_file)
print(f"Input lu : Grille {W}x{H}, {N} bâtiments, {M} antennes, récompense {R}")

placed_antennas, remaining = place_antennas(W, H, N, M, R, buildings, antennas)

print(f"Antennes placées : {len(placed_antennas)}")
print(f"Bâtiments non couverts : {remaining}")
if remaining == 0:
    print("Tous les bâtiments sont couverts !")
else:
    print(f"Optimisation supplémentaire nécessaire pour couvrir {remaining} bâtiments.")

with open(input_file[0] + "_output.txt", 'w') as f:
    f.write(f"{len(placed_antennas)}\n")
    for ant_id, x, y in placed_antennas:
        f.write(f"{ant_id} {x} {y}\n")

print(f"Temps d'exécution : {time.time() - start_time:.2f} secondes")