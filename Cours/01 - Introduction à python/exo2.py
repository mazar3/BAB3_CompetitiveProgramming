# 210668

with open("exo2_input.txt", "r") as f:
    lines = f.readlines()

N = int(lines[0])
results = []
index = 1

for i in range(N):
    G = int(lines[index])
    numbers = list(map(int, lines[index + 1].split()))
    unique_number = 0
    for num in numbers:
        unique_number ^= num
    results.append(f"Case #{i + 1}: {unique_number}")
    index += 2

with open("exo2_output.txt", "w") as f:
    f.write("\n".join(results))
