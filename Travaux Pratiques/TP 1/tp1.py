# 210668
import random
from operator import attrgetter

class Building:
    def __init__(self, x, y, l, c):
        self.x = x
        self.y = y
        self.l = l
        self.c = c
        self.his_antenna_id = -1

class Antenna:
    def __init__(self, id, r, c, w, h):
        self.id = id
        self.r = r
        self.c = c
        self.x = random.randint(0,w-1)
        self.y = random.randint(0,h-1)
        self.w = w
        self.h = h

class Instance:
    def __init__(self):
        self.n = 0
        self.m = 0
        self.r = 0
        self.buildings = []
        self.antennas = []
    def readfile(self, namefile):
        with open(namefile, 'r') as fin:
            a = list(map(int, fin.readline().split(' ')))
            w = a[0]
            h = a[1]
            b = list(map(int, fin.readline().split(' ')))
            self.n = b[0]
            self.m = b[1]
            self.r = b[2]
            for _ in range(1, self.n + 1):
                x, y, l, c = map(int, fin.readline().split(' '))
                self.buildings.append(Building(x, y, l, c))
            for i in range(0, self.m):
                r, c = map(int, fin.readline().split(' '))
                self.antennas.append(Antenna(i, r, c, w, h))

class Solution:
    def __init__(self, instance):
        self.instance = instance
        self.placed_antennas = []
        self.used_positions = set()
        self.building_scores = {b: 0 for b in instance.buildings}

    def calculate_potential_score(self, antenna, x, y):
        score = 0
        for building in self.instance.buildings:
            if building.his_antenna_id != -1:
                continue
            distance = abs(x - building.x) + abs(y - building.y)
            if distance <= antenna.r:
                new_score = building.c * antenna.c - building.l * distance
                if new_score > self.building_scores[building]:
                    score += new_score - self.building_scores[building]
        return score

    def place_antenna(self, antenna):
        best_score = -1
        best_position = (None, None)
        for building in sorted(self.instance.buildings,key=lambda b: (b.c * b.l, -b.x, -b.y),reverse=True):
            if building.his_antenna_id != -1:
                continue
            current_score = self.calculate_potential_score(antenna, building.x, building.y)
            if current_score > best_score and (building.x, building.y) not in self.used_positions:
                best_score = current_score
                best_position = (building.x, building.y)

        if best_position[0] is not None:
            antenna.x, antenna.y = best_position
            self.placed_antennas.append(antenna)
            self.used_positions.add(best_position)

            for building in self.instance.buildings:
                distance = abs(antenna.x - building.x) + abs(antenna.y - building.y)
                if distance <= antenna.r:
                    new_score = building.c * antenna.c - building.l * distance
                    if new_score > self.building_scores[building]:
                        self.building_scores[building] = new_score
                        building.his_antenna_id = antenna.id

    def writesol(self, filename):
        sorted_antennas = sorted(self.instance.antennas, key=lambda a: a.c * a.r, reverse=True)
        total_antennas = len(sorted_antennas)
        for idx, antenna in enumerate(sorted_antennas, 1):
            self.place_antenna(antenna)
            print(f"{idx}/{total_antennas} antennes placées...")
        uncovered_buildings = [b for b in self.instance.buildings if b.his_antenna_id == -1]
        if uncovered_buildings:
            remaining_antennas = [a for a in self.instance.antennas if a not in self.placed_antennas]
            for antenna in sorted(remaining_antennas, key=attrgetter('r'), reverse=True):
                for building in uncovered_buildings:
                    if (building.x, building.y) not in self.used_positions:
                        antenna.x, antenna.y = building.x, building.y
                        self.placed_antennas.append(antenna)
                        self.used_positions.add((building.x, building.y))
                        break


        sorted_antennas = sorted(self.placed_antennas, key=lambda a: a.id)
        with open(filename, 'w') as f:
            f.write(f"{len(sorted_antennas)}\n")
            for antenna in sorted_antennas:
                f.write(f"{antenna.id} {antenna.x} {antenna.y}\n")
        total_score = sum(solution.building_scores.values())
        print(f"Score total : {total_score}")


instance = Instance()
instance.readfile("c_metropolis.in")
solution = Solution(instance)
solution.writesol("tp1c_output.txt")