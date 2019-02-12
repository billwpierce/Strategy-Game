import sys
import pygame
import math
import hex_lib as lib
import tile_lib
import random
pygame.init()

# Game initialization
SIZE = WIDTH, HEIGHT = 960, 720
HEX_SIZE = 35
MAP_RADIUS = 5
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
tile_map = lib.generate_map(MAP_RADIUS)
layout = lib.Layout(lib.layout_flat, lib.Point(
    HEX_SIZE, HEX_SIZE), lib.Point(WIDTH/2, HEIGHT/2))

# Color setup
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_RED = (204, 89, 89)
RED = (140, 61, 61)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (120, 120, 120)
blue_team = tile_lib.Team("Blue", (89, 133, 204),
                          (117, 167, 246), (137, 187, 255))
red_team = tile_lib.Team("Red", (177, 90, 90),
                         (197, 110, 110), (217, 130, 130))

# Button constants
button_x_right = 13
button_y = 10
plus_width = 100+button_x_right
plus_height = 50+button_y
attack_button = pygame.Rect(WIDTH - plus_width, button_y, 100, 50)


def draw_hex(layout, hex, color=BLACK, width=1):
    pygame.draw.polygon(screen, color, lib.flat_hex_points(
        lib.hex_to_pixel(layout, hex), HEX_SIZE), width)


def draw_worth_circle(layout, tile, color=BLACK, width=0):
    center = (int(lib.hex_to_pixel(layout, tile.hex).x),
              int(lib.hex_to_pixel(layout, tile.hex).y))
    pygame.draw.circle(screen, color, center, tile.worth, 0)


def is_attack_ready(attack, defend):
    return (not (attack is None)) and (not (defend is None))


def update_tile_sets(tmap):
    owned_tiles = []
    blue_tiles = []
    red_tiles = []
    for _tile in tmap:
        if not (_tile.team is None):
            owned_tiles.append(_tile)
            if _tile.team.name == "Blue":
                blue_tiles.append(_tile)
            elif _tile.team.name == "Red":
                red_tiles.append(_tile)
    return owned_tiles, blue_tiles, red_tiles


def update_timer(clock, screen, time):
    screen.fill(WHITE)  # Clear the screen
    dt = clock.tick(30)
    _time = time + dt
    mspt = 2000  # milliseconds per cycle
    bar_len = 300  # length of the bar pixels
    cycles = math.floor(time/mspt)  # number of total cycles
    counter = time-(cycles*mspt)  # time in current cycle
    bar_fill = (counter*bar_len)/mspt  # How much to fill the bar in (pixels)
    pygame.draw.rect(screen, BLACK, pygame.Rect(
        26, HEIGHT-40, bar_len, 20), 1)  # Draw empty rectangle border
    pygame.draw.rect(screen, BLACK, pygame.Rect(
        26, HEIGHT-40, bar_fill, 20))  # Fill bar with counter
    return _time, cycles, counter


def tile_interact(attacking_tile, defending_tile, team_tiles):
    if is_attack_ready(attacking_tile, defending_tile):
        if not (defending_tile) in team_tiles:
            if attacking_tile.worth > defending_tile.worth:
                defending_tile.team = blue_team
                defending_tile.set_worth(
                    attacking_tile.worth - defending_tile.worth)
                attacking_tile.set_worth(0)
        else:
            ret = defending_tile.set_worth(
                defending_tile.worth + attacking_tile.worth)
            attacking_tile.worth = ret
    return attacking_tile, defending_tile


def click_tile(hovered, attacking_tile, defending_tile, tmap, team_tiles):
    if hovered in tmap:
        if hovered == attacking_tile:  # Reset both tiles
            attacking_tile = None
            defending_tile = None
        elif hovered == defending_tile:  # Reset defending tile
            defending_tile = None
        elif attacking_tile == None:  # Setting attack tile
            if hovered in team_tiles:
                attacking_tile = hovered
        elif defending_tile == None:  # setting defense tile
            if lib.tile_is_neighbor(attacking_tile, hovered):
                defending_tile = hovered
        else:
            defending_tile = None
            if lib.tile_is_neighbor(attacking_tile, hovered):
                attacking_tile = hovered
            else:
                attacking_tile = None
    return attacking_tile, defending_tile
