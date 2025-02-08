# 210668

class Building:
    def __init__(self, x, y, l, c):
        self.x = x
        self.y = y
        self.l = l
        self.c = c


class Antenna:
    def __init__(self, id, r, c):
        self.id = id
        self.r = r
        self.c = c


class Instance:
    def __init__(self):
        self.buildings = []
        self.antennas = []

    def readfile(self, namefile):
        with open(namefile, 'r') as file:
            lines = file.readlines()
            w, h = map(int, lines[0].split())
            n, m, r = map(int, lines[1].split())
            for i in range(2, 2 + n):
                x, y, l, c = map(int, lines[i].split())
                self.buildings.append(Building(x, y, l, c))
            for i in range(2 + n, 2 + n + m):
                r, c = map(int, lines[i].split())
                self.antennas.append(Antenna(len(self.antennas), r, c))


class Solution:
    def __init__(self, instance):
        self.instance = instance

    def writesol(self, namefile):
        with open(namefile, 'w') as file:
            file.write(f"{len(self.instance.antennas)}\n")
            for antenna in self.instance.antennas:
                file.write(f"{antenna.id} {antenna.r + antenna.c}\n")


instance = Instance()
instance.readfile("exo3_input.txt")
solution = Solution(instance)
solution.writesol("exo3_output.txt")