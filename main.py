import sys
import pygame
import math
import hex_lib as lib
import tile_lib
import random
from utility import *
pygame.init()

random.choice(tile_map[:len(tile_map)//2]).set_start(blue_team)
random.choice(tile_map[len(tile_map)//2:]).set_start(red_team)

attacking_tile = None
defending_tile = None

time = 0
cycle_cache = 0

while True:
    owned_tiles, blue_tiles, red_tiles = update_tile_sets(tile_map)
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
    mouse_pos = pygame.mouse.get_pos()

    if complete_move:
        attacking_tile, defending_tile = tile_interact(
            attacking_tile, defending_tile, blue_tiles)
        attacking_tile = defending_tile = None

    time, cycles, counter = update_timer(clock, screen, time)

    # Each cycle, do something
    if cycle_cache < cycles:
        cycle_cache = cycles
        for tile in owned_tiles:
            tile.grow()

    # Buttons
    if is_attack_ready(attacking_tile, defending_tile):
        if WIDTH-button_x_right > mouse_pos[0] > WIDTH-(plus_width) and button_y < mouse_pos[1] < plus_height:
            pygame.draw.rect(screen, LIGHT_RED, attack_button)
        else:
            pygame.draw.rect(screen, RED, attack_button)

    # Highlight hovered hex
    hovered = lib.mouse_to_tile(mouse_pos, layout, tile_map)
    if mouse_released:
        attacking_tile, defending_tile = click_tile(
            hovered, attacking_tile, defending_tile, tile_map, blue_tiles)

    # Draw tiles
    if not (hovered is None):
        draw_hex(layout, hovered.hex, width=0, color=LIGHT_GRAY)
    i = 0
    for _tile in tile_map:
        val = (i/len(tile_map))*255
        i += 1
        draw_hex(layout, _tile.hex, width=0, color=(
            val, val, val))  # draws the border
        if _tile.worth > 0:
            draw_worth_circle(layout, _tile)
    _relevant_blue = set()
    if attacking_tile:
        _relevant_blue.add(attacking_tile)
    if defending_tile:
        _relevant_blue.add(defending_tile)
    for item in blue_tiles:
        _relevant_blue.add(item)
    for _tile in _relevant_blue:
        _tile_color = None
        _tile_color = blue_team.color_main
        if _tile == attacking_tile:
            _tile_color = blue_team.color_attack
        if _tile == defending_tile:
            _tile_color = blue_team.color_victim
        draw_hex(layout, _tile.hex, width=4,
                 color=_tile_color)  # draws the border
    for _tile in red_tiles:
        _tile_color = red_team.color_main
        draw_hex(layout, _tile.hex, width=4,
                 color=_tile_color)
    pygame.display.flip()
