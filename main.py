import sys
import pygame
import math
import hex_lib as lib
import tile_lib
pygame.init()

SIZE = WIDTH, HEIGHT = 960, 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (120, 120, 120)

screen = pygame.display.set_mode(SIZE)

HEX_SIZE = 35
MAP_RADIUS = 5
tile_map = lib.generate_map(MAP_RADIUS)

layout = lib.Layout(lib.layout_flat, lib.Point(
    HEX_SIZE, HEX_SIZE), lib.Point(WIDTH/2, HEIGHT/2))


def draw_hex(layout, hex, color=BLACK, width=2):
    pygame.draw.polygon(screen, color, lib.flat_hex_points(
        lib.hex_to_pixel(layout, hex), HEX_SIZE), width)


selected = []

while True:
    # check for mouse events
    mouse_released = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_released = True

    screen.fill(WHITE)  # Clear the screen

    # Buttons
    pygame.draw.rect(screen, RED, (WIDTH-100, 0, 100, 50))

    # Map drawing functions

    # Highlight hovered hex
    hovered = lib.mouse_to_tile(pygame.mouse.get_pos(), layout, tile_map)
    if hovered in tile_map:
        if mouse_released:
            if hovered in selected:
                selected.remove(hovered)
            else:
                selected.append(hovered)
    if not (hovered is None):
        draw_hex(layout, hovered.hex, width=0, color=LIGHT_GRAY)
    for _tile in tile_map:
        if _tile in selected:
            draw_hex(layout, _tile.hex, width=0, color=DARK_GRAY)
        draw_hex(layout, _tile.hex)  # draws the border
    pygame.display.flip()
