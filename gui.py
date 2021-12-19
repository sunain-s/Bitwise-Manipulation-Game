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
    
    a_shift_button = pygame.Rect(767, 37, 224, 43)
    l_shift_button = pygame.Rect(767, 88, 224, 43)
    or_mask_button = pygame.Rect(706, 161, 168, 53)
    and_mask_button = pygame.Rect(706, 222, 168, 53)
    generate_button = pygame.Rect(277, 701, 230, 56)
    help_button_box = pygame.Rect(137, 697, 66, 66)
    mask_input_box = pygame.Rect(897, 165, 354, 107)
    a_shift_selected, l_shift_selected, or_mask_selected, and_mask_selected, help_selected, mask_input_selected, game_active = False, False, False, False, False, False, False

    denary_output_box = pygame.Rect(1096, 59, 153, 78)
    solution_output_box = pygame.Rect(767, 403, 428, 207)
    steps_output_box = pygame.Rect(1032, 630, 163, 135)
    target_bin_box = pygame.Rect(258, 267, 300, 50)
    current_bin_box = pygame.Rect(258, 425, 300, 50)

    left_triangle_boxes = [pygame.Rect(748, 36, 10, 96), pygame.Rect(738, 46, 10, 77), pygame.Rect(728, 54, 10, 59), pygame.Rect(718, 63, 10, 43), pygame.Rect(705, 77, 13, 15)]
    right_triangle_boxes = [pygame.Rect(1001, 36, 10, 96), pygame.Rect(1011, 46, 10, 77), pygame.Rect(1021, 54, 10, 59), pygame.Rect(1031, 63, 10, 43), pygame.Rect(1041, 77, 13, 15)]

    input_str = ''
    current_binary = ''
    target_binary = ''

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Constants

pygame.init()
CLOCK = pygame.time.Clock()
SCREEN_WIDTH = 1413
SCREEN_HEIGHT = 796
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bitwise Manipulation Game | Sunain Syed')
bg_image = pygame.image.load('bg_image.png')
font = pygame.font.Font('agency-fb-bold.ttf', 60)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Runs Program

if __name__ == '__main__':
    run()
