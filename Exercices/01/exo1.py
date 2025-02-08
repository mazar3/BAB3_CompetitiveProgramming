# 210668

with open("exo1_input.txt", "r") as f:
    lines = f.readlines()

C = int(lines[0])
results = []

for line in lines[1:]:
    data = list(map(int, line.split()))
    N = data[0]
    scores = data[1:]
    avg = sum(scores) / N
    above_avg = len([score for score in scores if score > avg])
    percentage = (above_avg / N) * 100
    results.append(f"{percentage:.3f}%")

with open("exo1_output.txt", "w") as f:
    f.write("\n".join(results))