N = int(input())

n_robots = 1
eta_with_sex = 1

while n_robots < N:
    n_robots *= 2
    eta_with_sex += 1

print(min(N, eta_with_sex))