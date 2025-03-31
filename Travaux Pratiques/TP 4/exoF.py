def inverse_factorial(n_factorial):
    if n_factorial == 0: return 1

    total_fact = 1
    for n in range(1, n_factorial + 1):
        total_fact *= n
        if total_fact == n_factorial :
            return n
    return False

print(inverse_factorial(int(input().strip())))