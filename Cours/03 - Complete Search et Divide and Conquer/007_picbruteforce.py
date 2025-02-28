v = [1, 3, 20, 4, 1, 0] 

for i in range(1,len(v)-1):
    if v[i] > v[i-1] and v[i] > v[i+1]:
        print(f'Pic en position {i+1} -> {v[i]}')