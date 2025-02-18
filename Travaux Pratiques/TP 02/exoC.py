# 210668

n, m = map(int, input().split())

verlan_dict = {}
for _ in range(n):
    correct, verlan = input().split()
    verlan_dict[verlan] = correct

mots_cherches = [input().strip() for _ in range(m)]

for mot in mots_cherches:
    print(verlan_dict.get(mot, "eh"))