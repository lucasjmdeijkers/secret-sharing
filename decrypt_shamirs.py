import ast

from encrypt_shamirs import program_ender, p
from time import sleep

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
            remaining_decimal = remaining_decimal // 2

            decimal_in_bits.insert(0, remainder)
        else:
            break

    # Splitting the whole secret into its individual characters using 8-bit splitting

    zero_pad = 8 - len(decimal_in_bits) % 8

    for zero in range(0, zero_pad):
        decimal_in_bits.insert(0, 0)

    decimal_as_byte = ''

    for bit in decimal_in_bits:
        decimal_as_byte += str(bit)

    n_chars = int(len(decimal_as_byte) / 8)

    # Rebuilding the secret from bits to ASCII values and then to characters

    split_bytes = []

    for char in range(0, n_chars):
        char_bytes = ''
        for bit in range(0, 8):
            string_bit = decimal_as_byte[0]
            decimal_as_byte = decimal_as_byte[1:]
            char_bytes += string_bit

        split_bytes.append(char_bytes)

        split_ascii = list(map(lambda byte: int(byte, 2), split_bytes))

        split_letters = list(map(lambda ascii_char: chr(ascii_char), split_ascii))

        concat_letters = ''

        for letter in split_letters:
            concat_letters += letter

    return concat_letters


def product_except_self(lst):
    n = len(lst)

    prod_list = []

    elements_before = 0
    elements_after = 0

    for pointer in range(n):
        prod = 1

        elements_after = (n - pointer - 1)
        elements_before = pointer

        for element in range(elements_before):
            prod = (prod * lst[element][0]) % p

        for element in range(1,elements_after+1):
            index = pointer + element
            prod = (prod * lst[index][0]) % p

        prod = prod % p
        prod_list.append(prod)

    return prod_list


def gaps(lst):
    n = len(lst)

    prod_gap_list = []

    elements_before = 0
    elements_after = 0

    for pointer in range(n):
        prod = 1

        elements_after = (n - pointer - 1)
        elements_before = pointer

        for element in range(elements_before):
            prod *= (lst[element][0] - lst[pointer][0]) % p

        for element in range(1,elements_after+1):
            index = pointer + element
            prod *= (lst[index][0] - lst[pointer][0]) % p


        prod_gap_list.append(prod)

    return prod_gap_list


def reconstruct_secret(shares: list) -> str:
    """
    This function reveals the secret when the threshold amount of shares are given.

    NOTE: a result is returned regardless of if the threshold is met, and there is no
    check to make sure whether it is or not. The 'revealed secret' will be nonsense if not enough
    shares are given

    :param shares: This is a list of the shares that are passed.
    :return: The revealed secret.
    """
    weight_dict = {}

    for i in range(len(shares)):
        # Fermat's litle theorem
        weight_dict[i] = product_except_self(shares)[i] * pow(gaps(shares)[i],p-2,p)

    reconstructed_secret = 0

    applied_weights = [weight_dict[i] * y for i,(x,y) in enumerate(shares)]

    for weighted_share in applied_weights:
        reconstructed_secret =  ( reconstructed_secret + weighted_share ) % p

    reconstructed_secret = reconstructed_secret % p

    return reconstructed_secret



if __name__ == "__main__":
    print("This program allows you to reveal an secret encrypted via Shamir's secret sharing algorithm.")
    print("Note: You must have the threshold number of shares as specified during encryption!\n")
    sleep(0.5)
    number_of_collected_shares = int(input("How many shares have you collected?: "))
    print("\n")
    sleep(0.5)
    print("Each share consists of two elements: (x,y).")
    print("Please enter both elements of each share in the correct order.")
    print("NOTE!: Do not include any leading or trailing whitespaces around or within the values")
    print("\n")
    sleep(0.5)

    shares = []

    for i in range(number_of_collected_shares):
        share = ast.literal_eval(input(f'Please enter the elements of share {i+1}: '))
        share = (share[0], share[1])
        shares.append(share)

    print("Thank you.\n")
    print("Decrypting", end="")
    sleep(0.5)
    print(".",end="")
    sleep(0.5)
    print(".",end="")
    sleep(0.5)
    print(".",end="\n")
    sleep(1)


    secret_in_decimal = reconstruct_secret(shares)

    secret_as_string = decimal_to_string(secret_in_decimal)

    print(f"Secret: {secret_as_string}")

    program_ender()


