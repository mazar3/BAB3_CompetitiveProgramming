n = int(input())
d_i = list(map(int, input().split()))
e_i = list(map(int, input().split()))

exercises = list(zip(d_i, e_i))

exercises.sort(key=lambda x: (x[1], x[0]))

cumulative_time = 0
max_late = 0
for d, e in exercises:
    cumulative_time += d
    delay = max(0, cumulative_time - e)
    max_late = max(max_late, delay)

print(max_late)