# NOTE: This is an educational implementation and should not be used
# for production cryptographic applications.

import secrets

NIST_P256_HEX = 'FFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF'
p = int(NIST_P256_HEX,16)

def program_ender():
    print(30 * '#')
    while input('Press "q" to close the program...') != 'q':
        print()
    quit()

def generate_shares(secret: str, threshold: int, shares: int) -> list:
    """
    This function simple coordinate shares to unlock an integer secret at a threshold number of shares.

    :param secret: This is a string of the secret you want to encrypt, e.g. "Lucas"
    :param threshold: This is the minimum number of shares required to decrypt the secret.
    :param shares: This is the number of shares you intend to distribute.
    :return: A list of tuples with the location of the shares on a Cartesian coordinate system
    """

    if isinstance(threshold, int):
        if threshold <= 0:
            print('Threshold must be atleast 1.')
            program_ender()

        if threshold > shares:
            print('Threshold must be smaller or equal to the share number.')
            program_ender()

    else:
        print('Threshold must be of type int.')
        program_ender()

    if isinstance(shares, int):
        if shares <= 0:
            print('Share number must be atleast 1.')
            program_ender()

    else:
        print('Shares must be of type int.')
        program_ender()

    polynomial_degree = threshold - 1

    # Building the polynomial
    coefficients = [secret]

    for i in range(0, polynomial_degree):
        coefficients.append(secrets.randbelow(p))

    # Building the share coordinates
    share_values = []

    for i in range(1,shares+1):
        x_coord = i
        y_coord = secret
        for degree in range(polynomial_degree, 0, -1):

            y_coord += (coefficients[degree]*pow(x_coord,degree,p)) % p

        share_value = [x_coord,y_coord]

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



    if isinstance(secret_as_string,str):
        if len(secret_as_string) == 0:
            print('Please enter at least one character as the secret!')
            program_ender()

    else:
        print('Secret must be a string.')
        program_ender()


    if any(ord(char) > 255 for char in secret_as_string):
        print('Secret must contain only ASCII characters.')
        program_ender()

    bytes_string = ''

    for char in secret_as_string:
        ascii_char = ord(char)
        bytes_char = str(format(ascii_char, '08b'))

        bytes_string += str(bytes_char)

    byte_decimal = 0

    # Big-Endian conversion of the 8-bit values to a unique decimal

    for bit in range(len(bytes_string)-1,-1,-1):
        byte_decimal += int(bytes_string[-(bit+1)]) * 2 ** bit

    return byte_decimal


def shamirs(secret: str, threshold: int, shares: int) -> list:
    """
    This function handles the full building of Shamirs secret sharing algorithm utilising sub-functions defined earlier.

    :param secret: This is a string of the secret you want to encrypt, e.g. "Lucas"
    :param threshold: This is the minimum number of shares required to decrypt the secret.
    :param shares: This is the number of shares you intend to distribute.
    :return: A list of tuples with the location of the shares on a Cartesian coordinate system
    """

    secret_in_decimal = secret_to_decimal(secret)
    if secret_in_decimal > p:
        print('Your secret is too complex.')
        program_ender()

    shares = generate_shares(secret_in_decimal, threshold, shares)

    return shares

if __name__ == "__main__":
    input_secret    = str(input("Please enter the passphrase you want to encrypt: "))
    try:
        input_shares_no = int(input("How many people do you want to give shares to?: "))
    except ValueError as e:
        print('Error! Please pass an integer.')
        program_ender()

    try:
        input_threshold = int(input("At a minimum, how many shares need to come together to decrypt the secret?: "))
    except ValueError as e:
        print('Error! Please pass an integer.')
        program_ender()

    shares_output = shamirs(input_secret, input_threshold, input_shares_no)

    print('These are the shares to distribute among your shareholders:')
    for share in shares_output:
        print(f'{share} \n')

    program_ender()


















