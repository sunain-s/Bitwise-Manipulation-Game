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

    denary = 0
    if binary[0] == '1': # checks if 7th bit is '1', if so -128
        denary += -128
    binary = binary[1:] # removes 7th bit to prevent from interfering with calculation
    power = 0
    for bit in binary[::-1]: #iterates through reversed binary string
        if bit == '1':
            denary += 2 ** power # adds increasing powers of 2 whenever a '1' is found
        power += 1
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
    print(binary)
    print(mask)
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
    print(binary)
    print(mask)
    masked_binary = ''
    for bit in range(len(binary)):
        if binary[bit] == '1' or mask[bit] == '1': # if '1' in either corresponding bit there is a '1'
            masked_binary += '1'
        else:
            masked_binary += '0' # otherwise '0'
        print(masked_binary)
    return zero_packing(masked_binary, 8)

# --------------------------------------------------------------------------------------------------
# Step Solving

def solve_in_one(target_binary, start_binary):
    '''
    Checks if target binary can be reached in 1 step, returns identifier code
    '''

    solve_code = 0 # default identifier code
    if logical_shift_mul(start_binary, 1) == target_binary: # checks if logical shift <== works
        solve_code = 1

    if logical_shift_div(start_binary, 1) == target_binary: # checks if logical shift ==> works
        solve_code = 2

    if arithmetic_shift_mul(start_binary, 1) == target_binary: # checks if arithmetic shift <== works
        solve_code = 3
    
    if arithmetic_shift_div(start_binary, 1) == target_binary: # checks if arithmetic shift ==> works
        solve_code = 4
    
    if and_mask(start_binary, target_binary) == target_binary: # checks if can be solved with an AND mask
        solve_code = 5
    
    if or_mask(start_binary, target_binary) == target_binary: # checks if can be solved with an OR mask
        solve_code = 6

    return solve_code

def solve_in_two(target_binary, start_binary):
    '''
    Solves all start to target possibilities:
        AND masking with '00000000' 
        OR masking with target binary
    '''

    and_mask_str = '00000000'
    binary = and_mask(start_binary, and_mask_str) # masks and turns binary to '00000000'
    binary = or_mask(binary, target_binary) # masks and creates target binary
    return and_mask_str, target_binary

# --------------------------------------------------------------------------------------------------
# Test Site
