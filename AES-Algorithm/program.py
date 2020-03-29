# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 09:34:23 2020

@author: Shashwat Kathuria
"""

# Number of columns in state
noOfColumns = 4
# Number of rounds in AES 128 cycle
noOfRounds = 10
# Key Length (in 32-bit words)
noOfWordsInKey = 4

def main():

    # Taking inputs from user
    print()
    plaintext = input('Enter the plaintext : ').encode()
    key = input('Enter key (must be less than 16 symbols and should consist of only alphabets & numbers) : ')
    print()

    # Checking if key is invalid
    if len(key) > 16:
        print('Invalid Key. Key too long.')
        return

    # Checking if key is invalid
    for symbol in key:
        if ord(symbol) > 0xff:
            print('Invalid Key. Please use only latin alphabet and numbers.')
            return

    # Encrypting message 16 bytes at a time
    encryptedBytes = []
    temp = []
    for byte in plaintext:
        temp.append(byte)
        if len(temp) == 16:
            Encrypted16Bytes = AES128Encryption(temp, key)
            encryptedBytes.extend(Encrypted16Bytes)
            temp = []

    # If plaintext is not a multiple of 16 bytes
    if 0 < len(temp) < 16:
            emptySpaces = 16 - len(temp)
            for i in range(emptySpaces - 1):
                temp.append(0)
            temp.append(1)
            Encrypted16Bytes = AES128Encryption(temp, key)
            encryptedBytes.extend(Encrypted16Bytes)

    # Encrypted message is now compulsorily a multiple of 16 bytes
    # Because padding is added.

    encryptedMessage = bytes(encryptedBytes)

    # Printed encrypted message
    print("Encrypted ciphertext is (in bytes) : ", encryptedMessage)

    # Decrypted 16 Bytes at a time
    decryptedBytes = []
    temp = []
    for byte in encryptedMessage:
        temp.append(byte)
        if len(temp) == 16:
            Decrypted16Bytes = AES128Decryption(temp, key)
            decryptedBytes.extend(Decrypted16Bytes)
            temp = []

    # Removing padding at the end
    decryptedMessage = bytes(decryptedBytes[ : -emptySpaces])

    # Printed decrypted message
    print("Decrypted plaintext is (in bytes) : ", decryptedMessage)
    print()

def AES128Encryption(plaintextBytes, key):
    """Function to implement AES Encryption Algorithm. Number of bytes should be equal to 16."""

    # Initializing state
    state = [[] for j in range(4)]

    # Adding values into state from plaintextBytes array into state matrix
    for row in range(4):
        for column in range(noOfColumns):
            state[row].append(plaintextBytes[row + 4 * column])

    # Expanding key
    keySchedule = keyExpansion(key)

    # Round 0, Adding round key only
    round = 0
    state = addRoundKey(state, keySchedule, round)

    # Performing round 1 to last round - 1 round of AES
    for round in range(1, noOfRounds):
        state = subBytes(state, False)
        state = shiftRows(state, False)
        state = mixColumns(state, False)
        state = addRoundKey(state, keySchedule, round)

    # Last round of AES
    state = subBytes(state, False)
    state = shiftRows(state, False)
    state = addRoundKey(state, keySchedule, round + 1)

    # Computing output
    output = [None for i in range(4 * noOfColumns)]
    for row in range(4):
        for column in range(noOfColumns):
            output[row + 4 * column] = state[row][column]

    # Returning output
    return output


def AES128Decryption(ciphertextBytes, key):
    """Function to implement AES Decryption Algorithm. Number of bytes should be equal to 16."""

    # Initializing state
    state = [[] for i in range(noOfColumns)]

    # Adding values into state from ciphertextBytes array into state matrix
    for row in range(4):
        for column in range(noOfColumns):
            state[row].append(ciphertextBytes[row + 4 * column])

    # Expanding key
    keySchedule = keyExpansion(key)

    # Starting from last round (in reverse, because decryption)
    state = addRoundKey(state, keySchedule, noOfRounds)

    # Performing rounds from last round -1 to first in reverse
    round = noOfRounds - 1
    for round in range(round, 0, -1):
        state = shiftRows(state, True)
        state = subBytes(state, True)
        state = addRoundKey(state, keySchedule, round)
        state = mixColumns(state, True)

    round -= 1

    # Round 0 in reverse
    state = shiftRows(state, True)
    state = subBytes(state, True)
    state = addRoundKey(state, keySchedule, round)

    # Computing output
    output = [None for i in range(4 * noOfColumns)]
    for row in range(4):
        for column in range(noOfColumns):
            output[row + 4 * column] = state[row][column]

    # Returning output
    return output

# Precomputed Sbox array constants
Sbox = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

# Precomputed inverse Sbox array constants
inverseSbox = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]

def subBytes(state, inverse):
    """Function to use Sbox or Inverse Sbox to determine subBytes value in the algorithm"""

    box = Sbox
    if inverse == True:
        box = inverseSbox

    # Substituting bytes according to box
    for i in range(len(state)):
        for j in range(len(state[i])):

            # Formula for computing sbox index row and column
            row = state[i][j] // 0x10
            column = state[i][j] % 0x10

            # 16 * round + column, because box is an array, not a matrix
            boxElement = box[16 * row + column]
            # Substituting value to state
            state[i][j] = boxElement

    # Returning state
    return state


def shiftRows(state, inverse):
    """Function to shift rows in the state matrix as done in the AES algorithm."""

    count = 1

    # Right shift for decryption
    if inverse == True:
        for i in range(1, noOfColumns):
            state[i] = rightShift(state[i], count)
            count += 1
    # Left shift for decryption
    else:
        for i in range(1, noOfColumns):
            state[i] = leftShift(state[i], count)
            count += 1

    # Returning state
    return state

def leftShift(array, count):
    """Left shift an array count times."""

    result = array[:]
    # Left shifting array by one in each loop
    for i in range(count):
        temp = result[1:]
        temp.append(result[0])
        result[:] = temp[:]

    # Returning shifted array
    return result


def rightShift(array, count):
    """Right shift an array count times."""

    result = array[:]
    # Right shifting array by one in each loop
    for i in range(count):
        temp = result[:-1]
        temp.insert(0, result[-1])
        result[:] = temp[:]

    # Returning shifted array
    return result


def mixColumns(state, inverse):
    """Mixing columns with the Galois field attributes as done in the AES algorithm.
       Multiplication of matrices takes place here."""

    # Matrix multiplication as done in the AES Algorithm
    for i in range(noOfColumns):

        # Matrix multiplication for decryption
        if inverse == True:
            s0 = multiplyBy0x0e(state[0][i]) ^ multiplyBy0x0b(state[1][i]) ^ multiplyBy0x0d(state[2][i]) ^ multiplyBy0x09(state[3][i])
            s1 = multiplyBy0x09(state[0][i]) ^ multiplyBy0x0e(state[1][i]) ^ multiplyBy0x0b(state[2][i]) ^ multiplyBy0x0d(state[3][i])
            s2 = multiplyBy0x0d(state[0][i]) ^ multiplyBy0x09(state[1][i]) ^ multiplyBy0x0e(state[2][i]) ^ multiplyBy0x0b(state[3][i])
            s3 = multiplyBy0x0b(state[0][i]) ^ multiplyBy0x0d(state[1][i]) ^ multiplyBy0x09(state[2][i]) ^ multiplyBy0x0e(state[3][i])
        # Matrix multiplication for encryption
        else:
            s0 = multiplyBy0x02(state[0][i]) ^ multiplyBy0x03(state[1][i]) ^ state[2][i] ^ state[3][i]
            s1 = state[0][i] ^ multiplyBy0x02(state[1][i]) ^ multiplyBy0x03(state[2][i]) ^ state[3][i]
            s2 = state[0][i] ^ state[1][i] ^ multiplyBy0x02(state[2][i]) ^ multiplyBy0x03(state[3][i])
            s3 = multiplyBy0x03(state[0][i]) ^ state[1][i] ^ state[2][i] ^ multiplyBy0x02(state[3][i])

        # Storing values into state
        state[0][i] = s0
        state[1][i] = s1
        state[2][i] = s2
        state[3][i] = s3

    # Returning state
    return state

# RCON matrix constants for key exansion as done in AES Algorithm
RCON = [
    [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36],
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
]

def keyExpansion(key):
    """Funtion to make list of keys for addRoundKey."""

    # Initializing key symbols array
    keySymbols = [ord(symbol) for symbol in key]

    # Padding if key is less than 16 symbols
    if len(keySymbols) < 4 * noOfWordsInKey:
        for i in range(4 * noOfWordsInKey - len(keySymbols)):
            keySymbols.append(0x01)

    # Making cipher key (base of key schedule)
    keySchedule = [[] for i in range(4)]
    for row in range(4):
        for column in range(noOfWordsInKey):
            keySchedule[row].append(keySymbols[row + 4 * column])

    # Continuing to key schedule
    for column in range(noOfWordsInKey, noOfColumns * (noOfRounds + 1)):

        if column % noOfWordsInKey == 0:
            # Shifting last - 1 column
            temp = [keySchedule[row][column - 1] for row in range(1, 4)]
            temp.append(keySchedule[0][column - 1])

            # Changing elements using Sbox
            for j in range(len(temp)):

                # Formulas to compute sbox row and column
                SboxRow = temp[j] // 0x10
                SboxColumn = temp[j] % 0x10

                # 16 * round + column, because box is an array, not a matrix
                SboxElement = Sbox[16 * SboxRow + SboxColumn]

                # Substituting value into temp
                temp[j] = SboxElement

            # XORing 3 columns as required
            for row in range(4):
                s = (keySchedule[row][column - 4]) ^ (temp[row]) ^ (RCON[row][int(column / noOfWordsInKey - 1)])
                keySchedule[row].append(s)

        else:
            # XORing two columns
            for row in range(4):
                s = keySchedule[row][column - 4] ^ keySchedule[row][column - 1]
                keySchedule[row].append(s)

    # Returning key schedule
    return keySchedule


def addRoundKey(state, keySchedule, round):
    """That transformation combines State and KeySchedule together. Xor
    of State and RoundSchedule(part of KeySchedule).
    """

    for column in range(noOfWordsInKey):

        # XORing as required as a part of KeySchedule
        s0 = state[0][column] ^ keySchedule[0][noOfColumns * round + column]
        s1 = state[1][column] ^ keySchedule[1][noOfColumns * round + column]
        s2 = state[2][column] ^ keySchedule[2][noOfColumns * round + column]
        s3 = state[3][column] ^ keySchedule[3][noOfColumns * round + column]

        # Storing values into state
        state[0][column] = s0
        state[1][column] = s1
        state[2][column] = s2
        state[3][column] = s3

    # Returning state
    return state

def multiplyBy0x02(number):
    """Function to multiply by 0x02 in Galois Space."""

    # Multiplying by 0x02 in Galois Space
    if number < 0x80:
        result = (number << 1)
    else:
        result = (number << 1) ^ 0x1b

    result = result % 0x100

    # Returning result
    return result


def multiplyBy0x03(number):
    """Function to multiply by 0x03 in Galois Space."""
    # Breaking into simpler parts
    return (multiplyBy0x02(number) ^ number)


def multiplyBy0x09(number):
    """Function to multiply by 0x09 in Galois Space."""
    # Breaking into simpler parts
    return multiplyBy0x02(multiplyBy0x02(multiplyBy0x02(number))) ^ number


def multiplyBy0x0b(number):
    """Function to multiply by 0x0b in Galois Space."""
    # Breaking into simpler parts
    return multiplyBy0x02(multiplyBy0x02(multiplyBy0x02(number))) ^ multiplyBy0x02(number) ^ number


def multiplyBy0x0d(number):
    """Function to multiply by 0x0d in Galois Space."""
    # Breaking into simpler parts
    return multiplyBy0x02(multiplyBy0x02(multiplyBy0x02(number))) ^ multiplyBy0x02(multiplyBy0x02(number)) ^ number


def multiplyBy0x0e(number):
    """Function to multiply by 0x0e in Galois Space."""
    # Breaking into simpler parts
    return multiplyBy0x02(multiplyBy0x02(multiplyBy0x02(number))) ^ multiplyBy0x02(multiplyBy0x02(number)) ^ multiplyBy0x02(number)

if __name__ == '__main__':
    main()
