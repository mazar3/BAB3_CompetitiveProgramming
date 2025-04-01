n, k = map(int, input().strip().split())
ids = list(map(int, input().strip().split()))

def sort(n, k, ids):
    left = 0
    right = n - 1
    while left < right:
        if ids[left] + ids[right] == k:
            return "yes"
        elif ids[left] + ids[right] < k:
            left += 1
        elif ids[left] + ids[right] > k:
            right -= 1

    return "no"

print(sort(n, k, ids))