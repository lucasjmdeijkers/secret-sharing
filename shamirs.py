import random
import time
from textwrap import wrap
from random import randrange, seed

#TODO: Use security safe pseudo-RNG from module 'secrets'
#TODO: Implement finite field modulo a prime for enhanced security and numerical stability
#TODO: Make shares customisable

# NOTE: AS-IS THIS ENCRYPTION ALGORITHM IS NOT SECURE FOR REAL-WORLD USES.

random.seed()

def generate_shares(secret: str, threshold: int, shares: int) -> list:
    """
    This function simple coordinate shares to unlock an integer secret at a threshold number of shares.

    :param secret: This is a string of the secret you want to encrypt, e.g. "Lucas"
    :param threshold: This is the minimum number of shares required to decrypt the secret.
    :param shares: This is the number of shares you intend to distribute.
    :return: A list of tuples with the location of the shares on a Cartesian coordinate system
    """

    # Initialises the coordinate of the secret (always at the y-intercept)
    secret_coord = tuple([0,secret])

    polynomial_degree = threshold - 1

    # Building the polynomial
    coefficients = [secret]

    for i in range(0, polynomial_degree):
        coefficients.append(random.randrange(1, 1000000000))

    # Building the share coordinates
    share_values = []

    for i in range(1,shares+1):
        x_coord = i
        y_coord = secret
        for degree in range(polynomial_degree, 0, -1):

            y_coord += coefficients[degree]*(x_coord)**degree

        share_value = [x_coord, y_coord]

        share_values.append(tuple(share_value))

    return share_values


def secret_to_decimal(secret_as_string: str) -> int:
    """
    This function converts a secret string to a unique decimal number using big endian conversion.
    This makes it possible to put the secret of the Cartesian coordinate system.

    :param secret_as_string: This is the secret string that needs to be converted to a unique decimal.
    :return: An integer representation of the string.
    """

    # Each character in the secret string is converted to its ascii character
    # And then to its 8-bit value

    bytes_string = ''

    for char in secret_as_string:
        ascii_char = ord(char)
        bytes_char = str(format(ascii_char, '08b'))

        bytes_string += str(bytes_char)

    bit_length = len(bytes_string)

    byte_decimal = 0

    # Big-Endian conversion of the 8-bit values to a unique decimal

    for bit in range(len(bytes_string)-1,-1,-1):
        byte_decimal += int(bytes_string[-(bit+1)]) * 2 ** bit

    return byte_decimal


def decimal_to_string(decimal: int) -> str:
    """
    This function converts a decimal deterministically to a string via successive integer division
    and fixed-width segmentation (8-bit).
    
    :param decimal: This is the secret as a decimal that is we want to reveal as a string
    :return: The secret as a string.
    """

    decimal_in_bits = []

    remaining_decimal = decimal

    # The successive division into a combined binary representation of each character.

    while True:
        if remaining_decimal >= 1:

            remainder = remaining_decimal % 2
            remaining_decimal = remaining_decimal//2

            decimal_in_bits.insert(0, remainder)
        else:
            break

    # Splitting the whole secret into its individual characters using 8-bit splitting

    zero_pad = 8 - len(decimal_in_bits) % 8

    for zero in range(0,zero_pad):
        decimal_in_bits.insert(0,0)

    decimal_as_byte = ''

    for bit in decimal_in_bits:
        decimal_as_byte += str(bit)

    n_chars = int(len(decimal_as_byte)/8)

    # Rebuilding the secret from bits to ASCII values and then to characters

    split_bytes = []

    for char in range(0,n_chars):
        char_bytes = ''
        for bit in range(0,8):
            string_bit = decimal_as_byte[0]
            decimal_as_byte = decimal_as_byte[1:]
            char_bytes += string_bit


        split_bytes.append(char_bytes)

        split_ascii = list(map(lambda byte: int(byte,2), split_bytes))

        split_letters = list(map(lambda ascii_char: chr(ascii_char), split_ascii))

        concat_letters = ''

        for letter in split_letters:
            concat_letters += letter


    return concat_letters

def shamirs(secret: str, threshold: int, shares: int) -> list:
    """
    This function handles the full building of Shamirs secret sharing algorithm utilising sub-functions defined earlier.

    :param secret: This is a string of the secret you want to encrypt, e.g. "Lucas"
    :param threshold: This is the minimum number of shares required to decrypt the secret.
    :param shares: This is the number of shares you intend to distribute.
    :return: A list of tuples with the location of the shares on a Cartesian coordinate system
    """

    secret_in_decimal = secret_to_decimal(secret)

    print(secret_in_decimal)

    shares = generate_shares(secret_in_decimal, threshold, shares)

    return shares












