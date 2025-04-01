n = int(input())

people = []
for _ in range(n):
    people.append(input())

suspects = set(people)
questions_asked = 0

while len(suspects) > 1 and questions_asked < n - 1:
    suspects_list = list(suspects)
    a, b = suspects_list[0], suspects_list[1]

    print(f"? {a} {b}")
    response = input()
    questions_asked += 1

    if response == "OUI":
        suspects.remove(b)
    else:
        suspects.remove(a)

print(f"! {next(iter(suspects))}")
