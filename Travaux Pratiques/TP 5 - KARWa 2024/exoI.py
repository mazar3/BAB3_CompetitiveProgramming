def solve_constant_step_optimization(distances):
    positions = [0]
    for d in distances:
        positions.append(positions[-1] + d)
    positions = positions[1:]

    candidates = set()
    for position in positions:
        for i in range(2, int(position ** 0.5) + 1):
            if position % i == 0:
                candidates.add(i)
                candidates.add(position // i)
        if position > 1:
            candidates.add(position)

    best_value = None
    best_result = 0

    for value in sorted(candidates):
        if value <= 1:
            continue

        result = sum(1 for position in positions if position % value == 0)

        if result > best_result:
            best_result = result
            best_value = value

    return best_value, best_result

n = int(input())
distances = [int(input()) for _ in range(n)]

result1, result2 = solve_constant_step_optimization(distances)
print(result1, result2)