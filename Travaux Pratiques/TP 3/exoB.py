from itertools import product

objective = int(input())
numbers = list(map(int, input().split()))

def can_construct(target, numbers):
    operations = ['+', '*', 'concat']
    n = len(numbers) - 1
    for ops in product(operations, repeat=n):
        result = numbers[0]
        for i in range(n):
            if ops[i] == '+':
                result += numbers[i + 1]
            elif ops[i] == '*':
                result *= numbers[i + 1]
            elif ops[i] == 'concat':
                result = int(str(result) + str(numbers[i + 1]))
        if result == target:
            return True
    return False

if can_construct(objective, numbers):
    print("YES")
else:
    print("NO")
