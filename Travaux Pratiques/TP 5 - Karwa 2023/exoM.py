import math

d = int(input())
alpha = int(input())

alpha_rad = math.radians(alpha)
distance = 2 * d * math.tan(alpha_rad)

print(distance)