import sys
import pygame
import math
import hex_lib as lib
pygame.init()

SIZE = WIDTH, HEIGHT = 960, 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (120, 120, 120)

SCREEN = pygame.display.set_mode(SIZE)

HEX_SIZE = 35
MAP_RADIUS = 5
MAP = lib.generate_map(MAP_RADIUS)

LAYOUT = lib.Layout(lib.layout_flat, lib.Point(
    HEX_SIZE, HEX_SIZE), lib.Point(WIDTH/2, HEIGHT/2))

selected = []

while True:
    mouse_released = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_released = True

    SCREEN.fill(WHITE)
    hovered = lib.mouse_to_hex(pygame.mouse.get_pos(), LAYOUT)
    if hovered in MAP:
        if mouse_released:
            if hovered in selected:
                selected.remove(hovered)
            else:
                selected.append(hovered)
        draw_hex(LAYOUT, hovered, width=0, color=LIGHT_GRAY)

    [draw_hex(LAYOUT, tile, width=0, color=DARK_GRAY) for tile in selected]
    [draw_hex(LAYOUT, tile) for tile in MAP]
    pygame.display.flip()


def draw_hex(layout, hex, color=BLACK, width=2):
    pygame.draw.polygon(SCREEN, color, lib.flat_hex_points(
        lib.hex_to_pixel(layout, hex), HEX_SIZE), width)
