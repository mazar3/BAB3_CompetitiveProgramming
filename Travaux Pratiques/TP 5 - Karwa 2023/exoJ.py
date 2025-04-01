def find_smallest_divisor(n):
    i = 2
    while i * i <= n:
        if n % i == 0:
            return i
        i += 1
    return n

n = int(input())
koalas_str = input().strip().split()
koalas = [int(k) for k in koalas_str]

koalas_with_divisors = [(k, find_smallest_divisor(k)) for k in koalas]

koalas_sorted = sorted(koalas_with_divisors, key=lambda x: (x[1], x[0]))

result = [k[0] for k in koalas_sorted]

print(' '.join(map(str, result)))