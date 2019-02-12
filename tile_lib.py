import hex_lib as lib
import random
import math


class Tile():

    def __init__(self, hex, worth=None, team=None):
        self.min = 1
        self.max = 21
        if worth is None:
            self.worth = random.randint(self.min, 7)
        else:
            self.worth = worth
        self.team = team
        self.hex = hex

    def set_worth(self, value):
        if value > self.max:
            self.worth = self.max
            return value - self.max
        elif value < self.min:
            self.worth = self.min
            return value - self.min
        else:
            self.worth = value
            return 0

    def set_start(self, team):
        self.team = team
        self.worth = math.ceil(self.max/2)

    def grow(self):
        self.set_worth(self.worth + random.randint(0, 2))


class Team():
    def __init__(self, name, color_main, color_attack, color_victim):
        self.name = name
        self.color_main = color_main
        self.color_attack = color_attack
        self.color_victim = color_victim
