import sys
import pygame
import math
import hex_lib
pygame.init()

size = width, height = 960, 720
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

def flat_hex_corner(centerx, centery, size, i): # From https://www.redblobgames.com/grids/hexagons/
    angle_deg = 60 * i
    angle_rad = (math.pi/180) * angle_deg
    # return hex_lib.Point(centerx + size * math.cos(angle_rad),centery+size*math.sin(angle_rad))
    return [centerx + size * math.cos(angle_rad), centery+size*math.sin(angle_rad)]

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    screen.fill(white)
    hex_points = [flat_hex_corner(100, 100, 25, i) for i in range(0, 6)]
    pygame.draw.lines(screen, black, True, hex_points, 2)
    # screen.blit(ball, ballrect)
    pygame.display.flip()
