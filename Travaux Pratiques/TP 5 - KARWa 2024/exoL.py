n = int(input())
m, k = map(int, input().split())
p = int(input())

print(max(n-(m*k-p),0))