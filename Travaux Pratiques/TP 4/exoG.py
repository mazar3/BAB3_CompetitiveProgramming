x = int(input())

def isPrime_v3(n):
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    k = 1
    while (6*k - 1)**2 <= n:
        if n % (6*k - 1) == 0 or n % (6*k + 1) == 0:
            return False
        k += 1
    return True

for i in range(1, int(x/2)+1):
    if isPrime_v3(i) and isPrime_v3(x-i):
        print(str(i) + "+" + str(x-i))