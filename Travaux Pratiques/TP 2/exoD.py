# 210668

from collections import deque

def rebalance(left, right):
    if len(left) > len(right) + 1:
        right.appendleft(left.pop())
    elif len(right) > len(left):
        left.append(right.popleft())

N = int(input())
left = deque()
right = deque()
results = []

for _ in range(N):
    instruction = input().split()
    op = int(instruction[0])
    value = int(instruction[1])

    if op == 1:
        right.append(value)
    elif op == 2:
        left.appendleft(value)
    elif op == 3:
        if len(left) < len(right):
            left.append(right.popleft())
        right.appendleft(value)
    elif op == 4:
        if value < len(left):
            results.append(left[value])
        else:
            results.append(right[value - len(left)])

    rebalance(left, right)

print("\n".join(map(str, results)))