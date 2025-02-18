# 210668

def assemble_pairs(cards):
    paquet = []
    for card in cards:
        if paquet and (paquet[-1] + card) % 2 == 0:
            paquet.pop()
        else:
            paquet.append(card)
    return len(paquet)

n = int(input())
cards = list(map(int, input().split()))
cards_paired = assemble_pairs(cards)

print(cards_paired)