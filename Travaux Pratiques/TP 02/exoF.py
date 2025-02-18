# 210668

from collections import Counter

freq = Counter(input())

odd_count = sum(1 for count in freq.values() if count % 2 != 0)

print(0 if odd_count <= 1 else odd_count - 1)