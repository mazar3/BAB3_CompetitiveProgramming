# 210668

N, Y = map(int, input().split())
correct_list = set(map(int, input().split()))

print(" ".join(str(i) for i in range(N) if i not in correct_list))
print(f"Vous avez reussi a esquiver {len(correct_list)} obstacles !")