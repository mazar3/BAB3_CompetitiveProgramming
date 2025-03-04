from collections import Counter

freq = Counter(char for char in input().lower() if char.isalpha())

freq_sorted = sorted(freq.values(), reverse=True)

beauty = sum(freq_sorted[i] * (26 - i) for i in range(len(freq_sorted)))

print(beauty)