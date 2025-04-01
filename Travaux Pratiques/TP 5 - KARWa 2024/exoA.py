n = int(input())

b_list = []
for _ in range(n):
    b_i = int(input())
    b_list.append(b_i)
buildings = list(zip(b_list, range(n)))
buildings_sorted = sorted(buildings, key=lambda x: (-x[0], x[1]))

c_list = [int(input()) for _ in range(n)]
c_sorted = sorted(c_list, reverse=True)

c_assigned = [0] * n
for i in range(n):
    original_index = buildings_sorted[i][1]
    c_assigned[original_index] = c_sorted[i]

for i in range(n):
    print(b_list[i] * c_assigned[i])