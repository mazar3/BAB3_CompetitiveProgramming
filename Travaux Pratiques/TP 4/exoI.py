k = int(input())

if k == 1:
    print(0, 1)
elif k == 2:
    print(1, 0)
else:
    f0 = 0
    f1 = 1
    for i in range(2, k):
        f2 = (f0 + f1) % (10 ** 9 + 7)
        f0 = f1
        f1 = f2
    print(f1, f0)