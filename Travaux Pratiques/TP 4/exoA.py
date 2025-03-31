n, r = map(int, input().split())

friends = [set() for _ in range(n)]
for _ in range(r):
    a, b = map(int, input().split())

    friends[a].add(b)
    friends[b].add(a)

friends_max = 0
for i in range(n):
    friends_max = max(friends_max, len(friends[i]))

print(friends_max)