n, a = map(int, input().strip().split())
valid_attractions = []

for _ in range(n):
    parts = input().strip().split()
    name = parts[0]
    m = int(parts[1])
    heights = list(map(int, parts[2:2 + m]))

    is_valid = True
    for i in range(len(heights) - 1):
        if heights[i] > heights[i + 1]:
            diff = heights[i] - heights[i + 1]
            if diff > a:
                is_valid = False
                break

    if is_valid:
        valid_attractions.append(name)

print(len(valid_attractions))
for attraction in valid_attractions:
    print(attraction)