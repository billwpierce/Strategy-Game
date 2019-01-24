import sys
import pygame
import math
import hex_lib as lib
import tile_lib
import random
pygame.init()

SIZE = WIDTH, HEIGHT = 960, 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_RED = (204, 89, 89)
RED = (140, 61, 61)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (120, 120, 120)
ATTACK_BLUE = (117, 167, 246)
OWNED_BLUE = (89, 133, 204)
DEFEND_RED = (177, 90, 90)

screen = pygame.display.set_mode(SIZE)

HEX_SIZE = 35
MAP_RADIUS = 5
tile_map = lib.generate_map(MAP_RADIUS)

layout = lib.Layout(lib.layout_flat, lib.Point(
    HEX_SIZE, HEX_SIZE), lib.Point(WIDTH/2, HEIGHT/2))


def draw_hex(layout, hex, color=BLACK, width=1):
    pygame.draw.polygon(screen, color, lib.flat_hex_points(
        lib.hex_to_pixel(layout, hex), HEX_SIZE), width)


def is_attack_ready(attack, defend):
    return (not (attack is None)) and (not (attack is None))


owned = []
owned.append(random.choice(tile_map))

attacking_tile = None
defending_tile = None

_button_x_right = 13
_button_y = 10
_plus_width = 100+_button_x_right
_plus_height = 50+_button_y
attack_button = pygame.Rect(WIDTH - _plus_width, _button_y, 100, 50)

while True:
    # check for mouse events
    mouse_released = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            mouse_released = True
            if attack_button.collidepoint(mouse_pos):
                print("clicked")
    mouse_pos = pygame.mouse.get_pos()

    screen.fill(WHITE)  # Clear the screen

    # Buttons
    if is_attack_ready(attacking_tile, defending_tile):
        if WIDTH-_button_x_right > mouse_pos[0] > WIDTH-(_plus_width) and _button_y < mouse_pos[1] < _plus_height:
            pygame.draw.rect(screen, LIGHT_RED, attack_button)
        else:
            pygame.draw.rect(screen, RED, attack_button)

    # Highlight hovered hex
    hovered = lib.mouse_to_tile(mouse_pos, layout, tile_map)
    if hovered in tile_map:
        if mouse_released:
            if hovered == attacking_tile:
                defending_tile = None
                attacking_tile = None
            elif hovered == defending_tile:
                defending_tile = None
            elif attacking_tile == None:
                attacking_tile = hovered
            elif defending_tile == None:
                defending_tile = hovered

    if not (hovered is None):
        draw_hex(layout, hovered.hex, width=0, color=LIGHT_GRAY)
    for _tile in tile_map:
        _tile_color = None
        if _tile in owned:
            _tile_color = OWNED_BLUE
        if _tile == attacking_tile:
            _tile_color = ATTACK_BLUE
        if _tile == defending_tile:
            _tile_color = DEFEND_RED
        if not (_tile_color is None):
            draw_hex(layout, _tile.hex, width=0, color=_tile_color)
        draw_hex(layout, _tile.hex)  # draws the border
    pygame.display.flip()
