# Lecture de l'input
n = int(input().strip())
row0 = input().strip()
row1 = input().strip()

# Fonction qui extrait les segments (début et fin indices) d'espaces vides d'une rangée
def get_segments(row):
    segments = []
    i = 0
    while i < len(row):
        if row[i] == '.':
            start = i
            while i < len(row) and row[i] == '.':
                i += 1
            end = i - 1
            segments.append((start, end))
        else:
            i += 1
    return segments

segments_top = get_segments(row0)
segments_bot = get_segments(row1)

# Le nombre de gardes si l'on ne fusionne pas :
nb_top = len(segments_top)
nb_bot = len(segments_bot)

# Pour économiser un garde, on peut fusionner un segment isolé (longueur 1)
# avec un segment de l'autre rangée recouvrant la même colonne.
# Nous allons construire un « appariement » entre segments_top et segments_bot
# et compter le nombre maximum de fusions possibles.
#
# Dans notre graphe bipartite, un segment du haut et un segment du bas
# sont "appariables" si leurs intervalles se chevauchent (c'est-à-dire si
# max(start_top, start_bot) <= min(end_top, end_bot)) et si l'un des deux est isolé.

# Pour faciliter l'appariement, nous trions les segments par leur borne droite (end).
segments_top.sort(key=lambda seg: seg[1])
segments_bot.sort(key=lambda seg: seg[1])

match = 0
i, j = 0, 0
while i < len(segments_top) and j < len(segments_bot):
    tstart, tend = segments_top[i]
    bstart, bend = segments_bot[j]
    # S'il n'y a pas de chevauchement
    if tend < bstart:
        i += 1
    elif bend < tstart:
        j += 1
    else:
        # Ils se chevauchent, vérifions si l'un des deux est isolé.
        if tstart == tend or bstart == bend:
            match += 1
            i += 1
            j += 1
        else:
            # Les deux segments couvrent plus d'une cellule : ils ne peuvent être fusionnés.
            # On avance celui qui se termine le plus tôt.
            if tend <= bend:
                i += 1
            else:
                j += 1

# Le nombre minimum de gardes est le nombre de segments moins le nombre de fusions réalisées.
result = nb_top + nb_bot - match
print(result)
