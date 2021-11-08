# Shifts and Mask operations

# --------------------------------------------------------------------------------------------------
# Logical Shifts
# 2**x, x>0: shifts <==  multiplying
# 2**x, x<0: shifts ==> dividing

# Arithmetic Shifts
# multiplying and dividing but for Two's Complement 
# retains leading 1s when shifting a negative binary number

# Masking
# AND - used to turn off bits: input(10011010) + mask(11100110) = output(10000010)
# OR - used to turn on bits: input(10011010) + mask(11100110) = output(1111110)

# --------------------------------------------------------------------------------------------------

def bin_to_den(binary):
    '''
    Converts binary strings to denary via addition method
    '''

    binary = binary[::-1]
    denary = 0
    power = 0
    for bit in binary:
        if bit == '1':
            denary += 2**power # addition method of converting
        power += 1 # uses place values
    return denary
