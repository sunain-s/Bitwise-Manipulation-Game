# Graphical Interface for Bitwise Manipulation Game

# Imports
import sys
import pygame
from operations import *

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Utility Functions

def draw_text(text, font, color, surface, x, y):
    '''
    Outputs text at the specified location, with (x,y) being the centre of the text object, using the required parameters
    '''

    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def input_valid(inp):
    for chr in inp:
        if chr != '1' and chr != '0':
            return False 
    return True

def draw_rect_transparent(surface, colour, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, colour, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main Function

def run():
    pass
