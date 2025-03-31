from collections import deque

N = int(input().strip())

graph = {}
for _ in range(N):
    parts = input().strip().split()
    station = parts[0]
    neighbors = parts[1:]

    if station not in graph:
        graph[station] = []

    for neighbor in neighbors:
        if neighbor not in graph:
            graph[neighbor] = []
        graph[station].append(neighbor)
        if station not in graph[neighbor]:
            graph[neighbor].append(station)

start, arrival = input().strip().split()

queue = deque([start])
parents = {start: None}
found_station = None

while queue:
    current = queue.popleft()
    if current == arrival:
        found_station = current
        break
    for neighbor in graph.get(current, []):
        if neighbor not in parents:
            parents[neighbor] = current
            queue.append(neighbor)

if found_station is None:
    print("pas de route")
else:
    path = []
    node = found_station
    while node is not None:
        path.append(node)
        node = parents[node]
    path.reverse()
    print(" ".join(path))