n = int(input())
d_i = list(map(int, input().split()))
e_i = list(map(int, input().split()))

d_i.sort()

cumulative_time = 0
total_time = 0
for d in d_i:
    cumulative_time += d
    total_time += cumulative_time

print(total_time // n)