def count_ways(n):
    mod = 7 + 10 ** 9
    if n == 1:
        return 1
    if n == 2:
        return 2

    def matrix_multiply(A, B):
        C = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
        return C

    def matrix_power(A, p):
        result = [[1, 0], [0, 1]]
        while p > 0:
            if p % 2 == 1:
                result = matrix_multiply(result, A)
            A = matrix_multiply(A, A)
            p //= 2
        return result

    A = [[1, 1], [1, 0]]
    A_n_minus_2 = matrix_power(A, n - 2)

    return (A_n_minus_2[0][0] * 2 + A_n_minus_2[0][1] * 1) % mod

n = int(input())
print(count_ways(n))