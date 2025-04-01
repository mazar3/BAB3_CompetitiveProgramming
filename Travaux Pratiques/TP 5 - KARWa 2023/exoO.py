n = int(input().strip())

max_hypotenuse = int(n * (2 ** 0.5)) + 1

palindromes = []
for i in range(1, min(10, max_hypotenuse + 1)):
    palindromes.append(i)

num_digits = 2
while 10 ** (num_digits - 1) <= max_hypotenuse:
    left_half_digits = num_digits // 2

    start = 10 ** (left_half_digits - 1)
    end = 10 ** left_half_digits

    for i in range(start, end):
        left_half = str(i)

        if num_digits % 2 == 1:
            for middle in range(10):
                palindrome = int(left_half + str(middle) + left_half[::-1])
                if palindrome <= max_hypotenuse:
                    palindromes.append(palindrome)
        else:
            palindrome = int(left_half + left_half[::-1])
            if palindrome <= max_hypotenuse:
                palindromes.append(palindrome)
    num_digits += 1

max_area_value = 0
for c in palindromes:
    if c / (2 ** 0.5) <= n:
        area = c ** 2 / 4
        max_area_value = max(max_area_value, area)

    elif c > n:
        other_side = (c ** 2 - n ** 2) ** 0.5
        if other_side <= n:
            area = (n * other_side) / 2
            max_area_value = max(max_area_value, area)

print(f"{max_area_value:.6f}")

