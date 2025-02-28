def peakDivideConquer(v,premier,dernier):
    milieu = (premier+dernier)//2
    if v[milieu+1] < v[milieu] > v[milieu-1]:
        return milieu
    elif v[milieu] > v[milieu+1]:
        return peakDivideConquer(v,milieu+1,dernier)
    elif v[milieu] < v[milieu-1]:
        return peakDivideConquer(v,premier,milieu-1)

v = [1, 3, 20, 4, 1, 0]
indice_pic = peakDivideConquer(v, 0, len(v)-1)
print(f'Pic en position {indice_pic}')