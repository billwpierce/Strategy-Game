import hex_lib as lib
import random


class Tile():
    def __init__(self, hex, worth=None):
        if worth is None:
            self.worth = random.randint(0, 7)
        else:
            self.worth = worth
        self.hex = hex
