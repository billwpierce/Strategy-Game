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
clock = pygame.time.Clock()


HEX_SIZE = 35
MAP_RADIUS = 5
tile_map = lib.generate_map(MAP_RADIUS)

layout = lib.Layout(lib.layout_flat, lib.Point(
    HEX_SIZE, HEX_SIZE), lib.Point(WIDTH/2, HEIGHT/2))


def draw_hex(layout, hex, color=BLACK, width=1):
    pygame.draw.polygon(screen, color, lib.flat_hex_points(
        lib.hex_to_pixel(layout, hex), HEX_SIZE), width)


def draw_worth_circle(layout, tile, color=BLACK, width=0):
    center = (int(lib.hex_to_pixel(layout, tile.hex).x),
              int(lib.hex_to_pixel(layout, tile.hex).y))
    pygame.draw.circle(screen, color, center, tile.worth, 0)


def is_attack_ready(attack, defend):
    return (not (attack is None)) and (not (defend is None))


owned = []
owned.append(random.choice(tile_map))
owned[0].worth = math.ceil(owned[0].max/2)

attacking_tile = None
defending_tile = None

_button_x_right = 13
_button_y = 10
_plus_width = 100+_button_x_right
_plus_height = 50+_button_y
attack_button = pygame.Rect(WIDTH - _plus_width, _button_y, 100, 50)
time = 0
cycle_cache = 0

while True:
    # check for mouse events
    mouse_released = False
    complete_move = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            mouse_released = True
            if attack_button.collidepoint(mouse_pos):
                complete_move = True
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_SPACE]:
                complete_move = True

    if complete_move:
        if is_attack_ready(attacking_tile, defending_tile):
            if not (defending_tile) in owned:
                if attacking_tile.worth > defending_tile.worth:
                    owned.append(defending_tile)
                    defending_tile.set_worth(
                        attacking_tile.worth - defending_tile.worth)
                    attacking_tile.set_worth(0)
                    attacking_tile = None
                    defending_tile = None
            else:
                ret = defending_tile.set_worth(
                    defending_tile.worth + attacking_tile.worth)
                attacking_tile.worth = ret
                attacking_tile = None
                defending_tile = None

    mouse_pos = pygame.mouse.get_pos()

    screen.fill(WHITE)  # Clear the screen
    dt = clock.tick(30)
    time += dt
    mspt = 2000  # milliseconds per cycle
    bar_len = 300  # length of the bar pixels
    cycles = math.floor(time/mspt)  # number of total cycles
    counter = time-(cycles*mspt)  # time in current cycle
    bar_fill = (counter*bar_len)/mspt  # How much to fill the bar in (pixels)
    pygame.draw.rect(screen, BLACK, pygame.Rect(
        26, HEIGHT-40, bar_len, 20), 1)  # Draw empty rectangle border
    pygame.draw.rect(screen, BLACK, pygame.Rect(
        26, HEIGHT-40, bar_fill, 20))  # Fill bar with counter

    # Do something on each cycle
    if cycle_cache < cycles:
        cycle_cache = cycles
        for tile in owned:
            if random.randint(0, 2) == 0:
                tile.set_worth(tile.worth + 1)

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
            if hovered == attacking_tile:  # Reset both tiles
                attacking_tile = None
                defending_tile = None
            elif hovered == defending_tile:  # Reset defending tile
                defending_tile = None
            elif attacking_tile == None:  # Setting attack tile
                if hovered in owned:
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

    # Draw tiles
    if not (hovered is None):
        draw_hex(layout, hovered.hex, width=0, color=LIGHT_GRAY)
    for _tile in tile_map:
        draw_hex(layout, _tile.hex)  # draws the border
        draw_worth_circle(layout, _tile)
    _relevant = set()
    if attacking_tile:
        _relevant.add(attacking_tile)
    if defending_tile:
        _relevant.add(defending_tile)
    for item in owned:
        _relevant.add(item)
    for _tile in _relevant:
        _tile_color = None
        if _tile in owned:
            _tile_color = OWNED_BLUE
        if _tile == attacking_tile:
            _tile_color = ATTACK_BLUE
        if _tile == defending_tile:
            _tile_color = DEFEND_RED
        draw_hex(layout, _tile.hex, width=4,
                 color=_tile_color)  # draws the border
    pygame.display.flip()
