# 210668

s = input()
bonbons = 0
resolus = set()
for c in s:
    if c in resolus:
        bonbons += 1
    else:
        bonbons += 2
        resolus.add(c)
print(bonbons)