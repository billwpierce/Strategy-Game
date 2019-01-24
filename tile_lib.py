import hex_lib as lib
import random


class Tile():
    def __init__(self, hex, worth=None):
        if worth is None:
            worth = random.randint(0, 7)
        self.hex = hex
