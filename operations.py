# Graphical Interface for Bitwise Manipulation Game

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
# Shifts and Mask operations

# --------------------------------------------------------------------------------------------------
# Imports

from random import randint

# --------------------------------------------------------------------------------------------------
# Logic Rules

'''
2**x, x>0: shifts <==  multiplying
2**x, x<0: shifts ==> dividing

Arithmetic Shifts
multiplying and dividing but for Two's Complement 
retains leading 1s when shifting a negative binary number

Masking
AND - used to turn off bits: input(10011010) + mask(11100110) = output(10000010)
OR - used to turn on bits: input(10011010) + mask(11100110) = output(1111110)
'''

# --------------------------------------------------------------------------------------------------
# Utility Functions

def zero_packing(binary, length):
    '''
    Packs binary string with zeros until a given length
        e.g. zero_packing('11001', 8)
    returns '00011001' which is in byte form
    '''

    binary = binary[::-1] # reverses binary string so it can be more easily packed with leading zeros
    if len(binary) % length:
        zeros = length - len(binary)
        binary += '0' * zeros  # packs necessary amount of leading zeros into string
    return binary[::-1] # returns binary

def one_packing(binary, length):
    '''
    Packs binary string with ones until a given length
        e.g. one_packing('11001', 8)
    returns '11111001' which is in byte form
    '''

    binary = binary[::-1] # reverses binary string so it can be more easily packed with leading ones
    if len(binary) % length:
        ones = length - len(binary)
        binary += '1' * ones  # packs necessary amount of leading ones into string
    return binary[::-1] # returns binary

def packing_check(binary):
    '''
    Checks if a binary string needs to be packed with 1s or 0s 
    Two's Complement is used at all times
    '''

    if binary[0] == '1': # checks sign bit
        binary = one_packing(binary, 8)
    if binary[0] == '0': # checks sign bit
        binary = zero_packing(binary, 8)
    return binary

# --------------------------------------------------------------------------------------------------
# Binary Stuff

def byte_to_denary(binary):
    '''
    Converts Two's Complement binary to denary, via addition method
    '''

    if len(binary) > 0:
        denary = 0
        if binary[0] == '1': # checks if 7th bit is '1', if so -128
            denary += -128
        binary = binary[1:] # removes 7th bit to prevent from interfering with calculation
        power = 0
        for bit in binary[::-1]: #iterates through reversed binary string
            if bit == '1':
                denary += 2 ** power # adds increasing powers of 2 whenever a '1' is found
            power += 1
    else:
        denary = ''
    return denary

def binary_generator():
    '''
    Creates a random 8 bit binary string
    '''

    byte = ''
    for bit in range(8):
        byte += str(randint(0, 1)) # concatenates random bit
    return byte

# --------------------------------------------------------------------------------------------------
# Shifting

def logical_shift_mul(binary ,shift_num):
    '''
    Performs logical shift multiplication (left lshift) on binary strings
        e.g. logical_shift_mul(10111000, 2) ==> 11100000 
    '''

    binary = packing_check(binary) # makes binary into appropriate byte form
    binary = bin(int(binary, 2) << shift_num) # performs left lshift
    binary = zero_packing(binary[2:], 8) # slices '0b' from string and packs with zeros
    return binary[abs(len(binary) - 8):] # slices to keep in byte form

def logical_shift_div(binary ,shift_num):
    '''
    Performs logical shift division (right lshift) on binary strings
        e.g. logical_shift_div(10111000, 2) ==> 00101110 
    '''
    
    binary = packing_check(binary) # makes binary into appropriate byte form
    binary = bin(int(binary, 2) >> shift_num) # performs right lshift
    binary = zero_packing(binary[2:], 8) # slices '0b' from string and packs with zeros
    return binary[abs(len(binary) - 8):] # slices to keep in byte form

def arithmetic_shift_div(binary, shift_num):
    '''
    Performs arithmetic shift division (right ashift) on binary strings
        e.g. arithmetic_shift_div(10111000, 1) ==> 11011100
    '''

    binary = packing_check(binary) # makes binary into appropriate byte form
    sign = binary[0] # saves sign bit
    binary = bin(int(binary, 2) >> shift_num) # performs right ashift
    binary = zero_packing(binary[2:], 8) # slices '0b' from string and packs with zeros
    binary = binary[abs(len(binary) - 8):] # slices to keep in byte form
    binary = sign + binary[1:] # replaces sign bit with original sign bit
    return binary 

# --------------------------------------------------------------------------------------------------
# Masking

def and_mask(binary, mask):
    '''
    AND Masks 2 8 bit binary strings together

    Truth Table:

    0   |   0   |   0
    0   |   1   |   0
    1   |   0   |   0
    1   |   1   |   1
        
    e.g.
             11011010
        AND  10111001
    output:  10011000
    '''

    binary = packing_check(binary) # makes binary into appropriate byte form
    mask = zero_packing(mask, 8) # makes mask into byte form
    masked_binary = ''
    for bit in range(len(binary)):
        if binary[bit] == '1' and mask[bit] == '1': # if '1' and '1' in corresponding bits there is a '1'
            masked_binary += '1'
        else:
            masked_binary += '0' # otherwise '0'
    return zero_packing(masked_binary, 8)

def or_mask(binary, mask):
    '''
    OR Masks 2 8 bit binary strings together

    Truth Table:

    0   |   0   |   0
    0   |   1   |   1
    1   |   0   |   1
    1   |   1   |   1
        
    e.g.
             11011010
        OR   10111001
    output:  11111011
    '''

    binary = packing_check(binary) # makes binary into appropriate byte form
    mask = zero_packing(mask, 8) # makes mask into byte form
    masked_binary = ''
    for bit in range(len(binary)):
        if binary[bit] == '1' or mask[bit] == '1': # if '1' in either corresponding bit there is a '1'
            masked_binary += '1'
        else:
            masked_binary += '0' # otherwise '0'
    return zero_packing(masked_binary, 8)

# --------------------------------------------------------------------------------------------------
# Step Solving

def solve_in_one(target_binary, start_binary):
    '''
    Checks if target binary can be reached in 1 step, returns identifier code
    '''

    solve_code = 5 # default identifier code
    if logical_shift_mul(start_binary, 1) == target_binary: # checks if logical shift <== works
        solve_code = 0

    if logical_shift_div(start_binary, 1) == target_binary: # checks if logical shift ==> works
        solve_code = 1
    
    if arithmetic_shift_div(start_binary, 1) == target_binary: # checks if arithmetic shift ==> works
        solve_code = 2
    
    if and_mask(start_binary, target_binary) == target_binary: # checks if can be solved with an AND mask
        solve_code = 3
    
    if or_mask(start_binary, target_binary) == target_binary: # checks if can be solved with an OR mask
        solve_code = 4

    return solve_code

# --------------------------------------------------------------------------------------------------
# Test Site

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

def animation_left(shift_string, box):
    time.sleep(.2)
    if len(shift_string) < 9:
        draw_text(shift_string, help_text_font, (0, 0, 0), SCREEN, box.centerx, box.centery + 40)
        shift_string += '<'
    else:
        shift_string = ''
    return shift_string

def animation_right(shift_string, box):
    time.sleep(0.2)
    if len(shift_string) < 9:
        draw_text(shift_string, help_text_font, (0, 0, 0), SCREEN, box.centerx, box.centery + 40)
        shift_string += '>'
    else:
        shift_string = ''
    return shift_string

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Help Screen Function

def help_screen():

    while True:

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
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main()

        CLOCK.tick(30)
        pygame.display.update()
        SCREEN.fill((20, 90, 115))

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main Function

def main():
    
    a_shift_button = pygame.Rect(767, 37, 224, 43)
    l_shift_button = pygame.Rect(767, 88, 224, 43)
    or_mask_button = pygame.Rect(706, 161, 168, 53)
    and_mask_button = pygame.Rect(706, 222, 168, 53)
    generate_button = pygame.Rect(277, 701, 230, 56)
    help_button_box = pygame.Rect(137, 697, 66, 66)
    mask_input_box = pygame.Rect(897, 165, 354, 107)
    a_shift_selected, l_shift_selected, or_mask_selected, and_mask_selected, mask_input_selected, game_active, solved, animate_left, animate_right = False, False, False, False, False, False, False, False, False

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
    steps = 0
    denary = ''
    shift_string = ''

    click = False
    while True:

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

        draw_rect_transparent(SCREEN, (255, 255, 255, 0), left_triangle_boxes[0])
        draw_rect_transparent(SCREEN, (255, 255, 255, 0), left_triangle_boxes[1])
        draw_rect_transparent(SCREEN, (255, 255, 255, 0), left_triangle_boxes[2])
        draw_rect_transparent(SCREEN, (255, 255, 255, 0), left_triangle_boxes[3])
        draw_rect_transparent(SCREEN, (255, 255, 255, 0), left_triangle_boxes[4])

        draw_rect_transparent(SCREEN, (255, 255, 255, 0), right_triangle_boxes[0])
        draw_rect_transparent(SCREEN, (255, 255, 255, 0), right_triangle_boxes[1])
        draw_rect_transparent(SCREEN, (255, 255, 255, 0), right_triangle_boxes[2])
        draw_rect_transparent(SCREEN, (255, 255, 255, 0), right_triangle_boxes[3])
        draw_rect_transparent(SCREEN, (255, 255, 255, 0), right_triangle_boxes[4])

        mx , my = pygame.mouse.get_pos()
        draw_text(input_str, font, (0, 0, 0), SCREEN, mask_input_box.centerx, mask_input_box.centery)
        draw_text(target_binary, font, (0, 0, 0), SCREEN, target_bin_box.centerx, target_bin_box.centery)
        draw_text(current_binary, font, (0, 0, 0), SCREEN, current_bin_box.centerx, current_bin_box.centery)
        draw_text(str(steps), help_title_font, (0, 0, 0), SCREEN, steps_output_box.centerx, steps_output_box.centery)
        draw_text(denary, font, (0, 0, 0), SCREEN, denary_output_box.centerx, denary_output_box.centery)

        denary = str(byte_to_denary(current_binary))

        if current_binary == target_binary and len(current_binary) > 0:
            solved = True
            game_active = False

        if generate_button.collidepoint(mx, my):
            if click:
                input_str = ''
                current_binary = binary_generator()
                target_binary = binary_generator()
                if current_binary == target_binary:
                    current_binary = binary_generator()
                start_binary = current_binary
                game_active = True
                solved = False
                steps = 0

        if help_button_box.collidepoint(mx, my):
            if click:
                a_shift_selected, l_shift_selected, or_mask_selected, and_mask_selected, mask_input_selected = False, False, False, False, False
                help_screen()

        if solved:
            
            game_active = False
            a_shift_selected, l_shift_selected, or_mask_selected, and_mask_selected, mask_input_selected = False, False, False, False, False
            solution_messages = [
                ['Logical left shift', f'{start_binary} ==> {target_binary}'],
                ['Logical right shift', f'{start_binary} ==> {target_binary}'],
                ['Arithmetic right shift', f'{start_binary} ==> {target_binary}'],
                [f'AND mask with {target_binary}', f'{start_binary} ==> {target_binary}'],
                [f'OR mask with {target_binary}', f'{start_binary} ==> {target_binary}'],
                ['AND mask with 00000000', f'{start_binary} ==> 00000000', f'OR mask with {target_binary}', f'00000000 ==> {target_binary}']
            ]

            x = 40
            messages = solution_messages[solve_in_one(target_binary, start_binary)]
            for message in messages:
                draw_text(message, help_text_font, (0, 0, 0), SCREEN, solution_output_box.centerx, solution_output_box.top + x)
                x += 40


        if game_active:

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

            if a_shift_selected or l_shift_selected:

                for box in left_triangle_boxes:
                    if box.collidepoint(mx, my):
                        if click:
                            animate_left = True
                            
                for box in right_triangle_boxes:
                    if box.collidepoint(mx, my):
                        if click:
                            animate_right = True

            if animate_left:
                shift_string = animation_left(shift_string, current_bin_box)
                if len(shift_string) > 8:
                    current_binary = logical_shift_mul(current_binary, 1)
                    steps += 1
                    animate_left = False
            
            if animate_right:
                shift_string = animation_right(shift_string, current_bin_box)
                if len(shift_string) > 8:
                    if l_shift_selected:
                        current_binary = logical_shift_div(current_binary, 1)
                    elif a_shift_selected:
                        current_binary = arithmetic_shift_div(current_binary, 1)
                    steps += 1
                    animate_right = False


        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True   

                if pygame.MOUSEBUTTONDOWN and mask_input_box.collidepoint(mx, my):
                    mask_input_selected = True
                    input_str = ''
            
            if or_mask_selected or and_mask_selected:
                if mask_input_selected:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            input_str = input_str[:-1]
                        elif event.key == pygame.K_RETURN:
                            mask_input_selected = False
                            valid_input = input_valid(input_str)
                            if valid_input:
                                if or_mask_selected:
                                    current_binary = or_mask(current_binary, input_str)
                                elif and_mask_selected:
                                    current_binary = and_mask(current_binary, input_str)
                                steps += 1
                            input_str = ''
                            
                        else:
                            input_str += event.unicode

        CLOCK.tick(30)
        pygame.display.update()
        SCREEN.blit(bg_image, (0, 0))



# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Constants

pygame.init()
CLOCK = pygame.time.Clock()
SCREEN_WIDTH = 1413
SCREEN_HEIGHT = 796
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bitwise Manipulation Game | Asianguy_123')
bg_image = pygame.image.load('bg_image.png')
font = pygame.font.Font('agency-fb-bold.ttf', 60)
help_title_font = pygame.font.Font('agency-fb-bold.ttf', 80)
help_text_font = pygame.font.Font('agency-fb-bold.ttf', 40)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Runs Program

if __name__ == '__main__':
    main()
