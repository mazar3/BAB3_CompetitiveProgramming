# 210668

input_string = input()
result = []
i = 0

while i < len(input_string):
    if input_string[i] == "\\":
        if result:
            result.pop()
        i += 1
    else:
        result.append(input_string[i])
        i += 1

print(''.join(result))
