# 210668

from collections import deque

N = int(input())
stack = []
queue = deque()
priority_queue = []

is_stack = True
is_queue = True
is_priority_queue = True

for _ in range(N):
    op_type, x = map(int, input().split())
    if op_type == 1:
        stack.append(x)
        queue.append(x)
        priority_queue.append(x)
        priority_queue.sort(reverse=True)
    elif op_type == 2:
        if not stack or not queue or not priority_queue:
            is_stack = is_queue = is_priority_queue = False
            break
        if stack.pop() != x:
            is_stack = False
        if queue.popleft() != x:
            is_queue = False
        if priority_queue.pop(0) != x:
            is_priority_queue = False

if sum([is_stack, is_queue, is_priority_queue]) > 1:
    print("pas sur")
elif is_stack:
    print("pile")
elif is_queue:
    print("file")
elif is_priority_queue:
    print("file prioritaire")
else:
    print("impossible")