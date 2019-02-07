import hex_lib as lib
import random


class Tile():

    def __init__(self, hex, worth=None):
        self.min = 1
        self.max = 21
        if worth is None:
            # self.worth = random.randint(self.min, 7)
            self.worth = 0
        else:
            self.worth = worth
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
