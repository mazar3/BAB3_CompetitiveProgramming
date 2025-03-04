A, N = map(int, input().split())
gains = [list(map(int, input().split())) for _ in range(N)]

tab = [0] * (A + 1)
for job_gains in gains:
    new_tab = tab[:]
    for a in range(A + 1):
        for k in range(A + 1):
            if a + k <= A:

                new_tab[a + k] = max(new_tab[a + k], tab[a] + job_gains[k])
    tab = new_tab

print(max(tab))