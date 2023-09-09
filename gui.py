# Graphical Interface for Bitwise Manipulation Game

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Imports
import sys
import pygame
from operations import *
import time

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
    '''
    Checks if mask input is valid - only contains 1s or 0s
    '''

    for chr in inp:
        if chr != '1' and chr != '0': 
            return False 
    return True

def draw_rect_transparent(surface, colour, rect):
    '''
    Draws transparent rectangles on given surface
    '''

    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA) # makes a surface from rectangles of given rectangles, with alpha property
    pygame.draw.rect(shape_surf, colour, shape_surf.get_rect()) # draws rectangle using surface
    surface.blit(shape_surf, rect) 

def animation_left(shift_string, box):
    '''
    Animation for left shifts
    '''

    time.sleep(.2)
    if len(shift_string) < 9:
        draw_text(shift_string, help_text_font, (0, 0, 0), SCREEN, box.centerx, box.centery + 40) # outputs animated string
        shift_string += '<' # extends string if string animation not complete
    else:
        shift_string = ''
    return shift_string

def animation_right(shift_string, box):
    '''
    Animation for right shifts
    '''

    time.sleep(0.2)
    if len(shift_string) < 9:
        draw_text(shift_string, help_text_font, (0, 0, 0), SCREEN, box.centerx, box.centery + 40) # outputs animated string
        shift_string += '>' # extends string if string animation not complete
    else:
        shift_string = ''
    return shift_string

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Help Screen Function

def help_screen():
    '''
    Help GUI for user instructions and explanation
    '''

    while True:

        # drawing all messages
        draw_text('Bitwise Manipulation Game', help_title_font, (255, 255, 255), SCREEN, SCREEN_WIDTH/2, 50)
        draw_text('Change your current binary into the target binary with as few steps as possible', help_text_font, (255, 255, 255), SCREEN, SCREEN_WIDTH/2, 140)
        draw_text('You can use logical shift, arithmetic shift, AND masking or OR masking to reach the target', help_text_font, (255, 255, 255), SCREEN, SCREEN_WIDTH/2, 190)
        draw_text('To start the game, click the generate button and your binaries will appear', help_text_font, (255, 255, 255), SCREEN, SCREEN_WIDTH/2, 270)
        draw_text('To perform a mask, select the type of mask and click the input box next to it and type the mask in', help_text_font, (255, 255, 255), SCREEN, SCREEN_WIDTH/2, 320)
        draw_text('and hit enter to submit it', help_text_font, (255, 255, 255), SCREEN, SCREEN_WIDTH/2, 370)
        draw_text('To perform a shift, select the mode then use the right and left arrows to shift', help_text_font, (255, 255, 255), SCREEN, SCREEN_WIDTH/2, 450)
        draw_text('Switch between logical and arithmetic shift by reselecting the mode', help_text_font, (255, 255, 255), SCREEN, SCREEN_WIDTH/2, 500)
        draw_text('Once you reach the target binary, the quickest solution will be shown', help_text_font, (255, 255, 255), SCREEN, SCREEN_WIDTH/2, 580)
        draw_text('To play again click the generate button and receive new binaries', help_text_font, (255, 255, 255), SCREEN, SCREEN_WIDTH/2, 630)
        draw_text('Press ESC to return to the game', help_text_font, (255, 255, 255), SCREEN, SCREEN_WIDTH/2, 730)
        
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

            # escape to main window
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main()

        CLOCK.tick(30)
        pygame.display.update()
        SCREEN.fill((20, 90, 115))

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main Function

def main():
    '''
    Main GUI function
    '''
    
    # button hitboxes
    a_shift_button = pygame.Rect(767, 37, 224, 43)
    l_shift_button = pygame.Rect(767, 88, 224, 43)
    or_mask_button = pygame.Rect(706, 161, 168, 53)
    and_mask_button = pygame.Rect(706, 222, 168, 53)
    generate_button = pygame.Rect(277, 701, 230, 56)
    help_button_box = pygame.Rect(137, 697, 66, 66)
    mask_input_box = pygame.Rect(897, 165, 354, 107)

    # booleans
    a_shift_selected, l_shift_selected, or_mask_selected, and_mask_selected, mask_input_selected, game_active, solved, animate_left, animate_right = False, False, False, False, False, False, False, False, False

    # output boxes
    denary_output_box = pygame.Rect(1096, 59, 153, 78)
    solution_output_box = pygame.Rect(767, 403, 428, 207)
    steps_output_box = pygame.Rect(1032, 630, 163, 135)
    target_bin_box = pygame.Rect(258, 267, 300, 50)
    current_bin_box = pygame.Rect(258, 425, 300, 50)

    # arrow boxes
    left_triangle_boxes = [pygame.Rect(748, 36, 10, 96), pygame.Rect(738, 46, 10, 77), pygame.Rect(728, 54, 10, 59), pygame.Rect(718, 63, 10, 43), pygame.Rect(705, 77, 13, 15)]
    right_triangle_boxes = [pygame.Rect(1001, 36, 10, 96), pygame.Rect(1011, 46, 10, 77), pygame.Rect(1021, 54, 10, 59), pygame.Rect(1031, 63, 10, 43), pygame.Rect(1041, 77, 13, 15)]

    # output strings/digits
    input_str = ''
    current_binary = ''
    target_binary = ''
    steps = 0
    denary = ''
    shift_string = ''

    click = False
    while True:

        # drawing invisible output and hitboxes
        draw_rect_transparent(SCREEN, (0, 0, 0, 0), a_shift_button)
        draw_rect_transparent(SCREEN, (0, 0, 0, 0), l_shift_button)
        draw_rect_transparent(SCREEN, (0, 0, 0, 0), or_mask_button)
        draw_rect_transparent(SCREEN, (0, 0, 0, 0), and_mask_button)
        draw_rect_transparent(SCREEN, (0, 0, 0, 0), denary_output_box)
        draw_rect_transparent(SCREEN, (0, 0, 0, 0), mask_input_box)
        draw_rect_transparent(SCREEN, (0, 0, 0, 0), solution_output_box)
        draw_rect_transparent(SCREEN, (0, 0, 0, 0), steps_output_box)
        draw_rect_transparent(SCREEN, (0, 0, 0, 0), target_bin_box)
        draw_rect_transparent(SCREEN, (0, 0, 0, 0), current_bin_box)
        draw_rect_transparent(SCREEN, (0, 0, 0, 0), help_button_box)
        draw_rect_transparent(SCREEN, (0, 0, 0, 0), generate_button)

        # drawing left shift invisble hitboxes
        draw_rect_transparent(SCREEN, (255, 255, 255, 0), left_triangle_boxes[0])
        draw_rect_transparent(SCREEN, (255, 255, 255, 0), left_triangle_boxes[1])
        draw_rect_transparent(SCREEN, (255, 255, 255, 0), left_triangle_boxes[2])
        draw_rect_transparent(SCREEN, (255, 255, 255, 0), left_triangle_boxes[3])
        draw_rect_transparent(SCREEN, (255, 255, 255, 0), left_triangle_boxes[4])

        # drawing right shift invisible hitboxes
        draw_rect_transparent(SCREEN, (255, 255, 255, 0), right_triangle_boxes[0])
        draw_rect_transparent(SCREEN, (255, 255, 255, 0), right_triangle_boxes[1])
        draw_rect_transparent(SCREEN, (255, 255, 255, 0), right_triangle_boxes[2])
        draw_rect_transparent(SCREEN, (255, 255, 255, 0), right_triangle_boxes[3])
        draw_rect_transparent(SCREEN, (255, 255, 255, 0), right_triangle_boxes[4])

        mx, my = pygame.mouse.get_pos() # gets mouse position

        # outputing strings and digits
        draw_text(input_str, font, (0, 0, 0), SCREEN, mask_input_box.centerx, mask_input_box.centery)
        draw_text(target_binary, font, (0, 0, 0), SCREEN, target_bin_box.centerx, target_bin_box.centery)
        draw_text(current_binary, font, (0, 0, 0), SCREEN, current_bin_box.centerx, current_bin_box.centery)
        draw_text(str(steps), help_title_font, (0, 0, 0), SCREEN, steps_output_box.centerx, steps_output_box.centery)
        draw_text(denary, font, (0, 0, 0), SCREEN, denary_output_box.centerx, denary_output_box.centery)
        denary = str(byte_to_denary(current_binary))

        # end game condition
        if current_binary == target_binary and len(current_binary) > 0:
            solved = True
            game_active = False

        # generate selected, begin game
        if generate_button.collidepoint(mx, my):
            if click:
                input_str = ''
                current_binary = binary_generator()
                target_binary = binary_generator()
                if current_binary == target_binary: # recreates current binary if already equal to
                    current_binary = binary_generator()
                start_binary = current_binary
                game_active = True
                solved = False
                steps = 0

        # if help selected, open help gui
        if help_button_box.collidepoint(mx, my):
            if click:
                a_shift_selected, l_shift_selected, or_mask_selected, and_mask_selected, mask_input_selected = False, False, False, False, False
                help_screen()

        # if game over
        if solved:
            
            game_active = False
            a_shift_selected, l_shift_selected, or_mask_selected, and_mask_selected, mask_input_selected = False, False, False, False, False

            # possible optimal solution messages
            solution_messages = [
                ['Logical left shift', f'{start_binary} ==> {target_binary}'],
                ['Logical right shift', f'{start_binary} ==> {target_binary}'],
                ['Arithmetic right shift', f'{start_binary} ==> {target_binary}'],
                [f'AND mask with {target_binary}', f'{start_binary} ==> {target_binary}'],
                [f'OR mask with {target_binary}', f'{start_binary} ==> {target_binary}'],
                ['AND mask with 00000000', f'{start_binary} ==> 00000000', f'OR mask with {target_binary}', f'00000000 ==> {target_binary}']
            ]

            # outputs appropriate message
            x = 40
            messages = solution_messages[solve_in_one(target_binary, start_binary)]
            for message in messages:
                draw_text(message, help_text_font, (0, 0, 0), SCREEN, solution_output_box.centerx, solution_output_box.top + x)
                x += 40

        # if game ongoing
        if game_active:

            # setting booleans for box clicks
            if a_shift_button.collidepoint(mx, my):
                if click:
                    a_shift_selected, l_shift_selected, or_mask_selected, and_mask_selected, mask_input_selected = True, False, False, False, False

            if l_shift_button.collidepoint(mx, my):
                if click:
                    a_shift_selected, l_shift_selected, or_mask_selected, and_mask_selected, mask_input_selected = False, True, False, False, False
            
            if or_mask_button.collidepoint(mx, my):
                if click:
                    a_shift_selected, l_shift_selected, or_mask_selected, and_mask_selected, mask_input_selected = False, False, True, False, False

            if and_mask_button.collidepoint(mx, my):
                if click:
                    a_shift_selected, l_shift_selected, or_mask_selected, and_mask_selected, mask_input_selected = False, False, False, True, False

            # checking left or right shift clicks
            if a_shift_selected or l_shift_selected:

                for box in left_triangle_boxes:
                    if box.collidepoint(mx, my):
                        if click:
                            animate_left = True
                            
                for box in right_triangle_boxes:
                    if box.collidepoint(mx, my):
                        if click:
                            animate_right = True

            # animating for left shift, and shifting binary
            if animate_left:
                shift_string = animation_left(shift_string, current_bin_box)
                if len(shift_string) > 8:
                    current_binary = logical_shift_mul(current_binary, 1)
                    steps += 1
                    animate_left = False
            
            # animating for right shift, and shifting binary
            if animate_right:
                shift_string = animation_right(shift_string, current_bin_box)
                if len(shift_string) > 8:
                    if l_shift_selected:
                        current_binary = logical_shift_div(current_binary, 1)
                    elif a_shift_selected:
                        current_binary = arithmetic_shift_div(current_binary, 1)
                    steps += 1
                    animate_right = False

        # event loop
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            
            # click input check
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True   

                # check if input box selected
                if pygame.MOUSEBUTTONDOWN and mask_input_box.collidepoint(mx, my):
                    mask_input_selected = True
                    input_str = ''
            
            # mask input
            if or_mask_selected or and_mask_selected:
                if mask_input_selected:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            input_str = input_str[:-1] # deleting
                        elif event.key == pygame.K_RETURN: # submitting mask input
                            mask_input_selected = False 
                            valid_input = input_valid(input_str) # input validity check
                            if valid_input: # performs mask
                                if or_mask_selected:
                                    current_binary = or_mask(current_binary, input_str) 
                                elif and_mask_selected:
                                    current_binary = and_mask(current_binary, input_str)
                                steps += 1
                            input_str = '' # resets mask input                            
                        else:
                            input_str += event.unicode # adds input to string

        CLOCK.tick(30)
        pygame.display.update()
        SCREEN.blit(bg_image, (0, 0)) # display background image

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
help_title_font = pygame.font.Font('agency-fb-bold.ttf', 80)
help_text_font = pygame.font.Font('agency-fb-bold.ttf', 40)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Runs Program

if __name__ == '__main__':
    main()
