n = int(input().strip())

passwords = []
for _ in range(n):
    password, prob = map(str, input().strip().split())
    prob = float(prob)
    passwords.append((password, prob))

passwords.sort(key=lambda x: x[1], reverse=True)

avg_time = 0
for i, (_, probability) in enumerate(passwords, 1):
    avg_time += i * probability

print(f"{avg_time:.4f}")