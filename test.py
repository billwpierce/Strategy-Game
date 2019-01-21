import sys
import pygame
import math
import hex_lib as hlib
pygame.init()

SIZE = WIDTH, HEIGHT = 1280, 960
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (120, 120, 120)

SCREEN = pygame.display.set_mode(SIZE)

HEX_SIZE = 35
MAP_RADIUS = 6
MAP = []

for q in range(-MAP_RADIUS, MAP_RADIUS+1): # From redblobgames
    r1 = max(-MAP_RADIUS, -q - MAP_RADIUS)
    r2 = min(MAP_RADIUS, -q + MAP_RADIUS)
    for r in range(r1, r2+1):
        MAP.append(hlib.Hex(q, r, -q-r))

LAYOUT = hlib.Layout(hlib.layout_flat, hlib.Point(HEX_SIZE, HEX_SIZE), hlib.Point(WIDTH/2, HEIGHT/2))

selected = []


def flat_hex_corner(center, size, i): # From https://www.redblobgames.com/grids/hexagons/
    angle_deg = 60 * i
    angle_rad = math.pi / 180 * angle_deg
    return [center.x + size * math.cos(angle_rad), center.y+size*math.sin(angle_rad)]

def flat_hex_points(center, size):
    return [flat_hex_corner(center, size, i) for i in range(0, 6)]

def draw_hex(layout, hex, color=BLACK, width=2):
    pygame.draw.polygon(SCREEN, color, flat_hex_points(hlib.hex_to_pixel(layout, hex), HEX_SIZE), width)

def mouse_to_point(mouse):
    return hlib.Point(mouse[0], mouse[1])

def mouse_to_hex(mouse):
    return hlib.hex_round(hlib.pixel_to_hex(LAYOUT, mouse_to_point(mouse)))

while 1:
    mouse_released = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_released = True

    SCREEN.fill(WHITE)
    hovered = mouse_to_hex(pygame.mouse.get_pos())
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
