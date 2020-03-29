# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:46:19 2020

@author: Shashwat Kathuria
"""

def main():

    print()
    # Taking inputs from the user
    plaintext = input("Enter the message to be encrypted : ")
    key = input("Enter a key of 8 length (64-bits) (characters or numbers only) : ")
    print()

    # Checking if key is valid or not
    if len(key) != 8:
        print("Invalid Key. Key should be of 8 length (8 bytes).")
        return

    # Determining if padding is required
    isPaddingRequired = (len(plaintext) % 8 != 0)

    # Encryption
    ciphertext = DESEncryption(key, plaintext, isPaddingRequired)

    # Decryption
    plaintext = DESDecryption(key, ciphertext, isPaddingRequired)

    # Printing result
    print()
    print("Encrypted Ciphertext is : %r " % ciphertext)
    print("Decrypted plaintext is  : ", plaintext)
    print()

# Permutation Matrix used after each SBox substitution for each round
eachRoundPermutationMatrix = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

# Final Permutation Matrix for data after 16 rounds
finalPermutationMatrix = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]


def DESEncryption(key, text, padding):
    """Function for DES Encryption."""

    # Adding padding if required
    if padding == True:
        text = addPadding(text)

    # Encryption
    ciphertext = DES(text, key, padding, True)

    # Returning ciphertext
    return ciphertext

def DESDecryption(key, text, padding):
    """Function for DES Decryption."""

    # Decryption
    plaintext = DES(text, key, padding, False)

    # Removing padding if required
    if padding == True:
        # Removing padding and returning plaintext
        return removePadding(plaintext)

    # Returning plaintext
    return plaintext

# Initial Permutation Matrix for data
initialPermutationMatrix = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

#Expand matrix to get a 48bits matrix of datas to apply the xor with Ki
expandMatrix = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]


def DES(text, key, padding, isEncrypt):
    """Function to implement DES Algorithm."""

    # Initializing variables required
    isDecrypt = not isEncrypt
    # Generating keys
    keys = generateKeys(key)

    # Splitting text into 8 byte blocks
    plaintext8byteBlocks = nSplit(text, 8)
    result = []

    # For all 8-byte blocks of text
    for block in plaintext8byteBlocks:

        # Convert the block into bit array
        block = stringToBitArray(block)

        # Do the initial permutation
        block = permutation(block, initialPermutationMatrix)

        # Splitting block into two 4 byte (32 bit) sized blocks
        leftBlock, rightBlock = nSplit(block, 32)

        temp = None

        # Running 16 identical DES Rounds for each block of text
        for i in range(16):
            # Expand rightBlock to match round key size(48-bit)
            expandedRightBlock = expand(rightBlock, expandMatrix)

            # Xor right block with appropriate key
            if isEncrypt == True:
                # For encryption, starting from first key in normal order
                temp = xor(keys[i], expandedRightBlock)
            elif isDecrypt == True:
                # For decryption, starting from last key in reverse order
                temp = xor(keys[15 - i], expandedRightBlock)
            # Sbox substitution Step
            temp = SboxSubstitution(temp)
            # Permutation Step
            temp = permutation(temp, eachRoundPermutationMatrix)
            # XOR Step with leftBlock
            temp = xor(leftBlock, temp)

            # Blocks swapping
            leftBlock = rightBlock
            rightBlock = temp

        # Final permutation then appending result
        result += permutation(rightBlock + leftBlock, finalPermutationMatrix)

    # Converting bit array to string
    finalResult = bitArrayToString(result)

    return finalResult

# Matrix used for shifting after each round of keys
SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Permutation matrix for key
keyPermutationMatrix1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# Permutation matrix for shifted key to get next key
keyPermutationMatrix2 = [
    14, 17, 11, 24, 1, 5, 3, 28,
    15, 6, 21, 10, 23, 19, 12, 4,
    26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40,
    51, 45, 33, 48, 44, 49, 39, 56,
    34, 53, 46, 42, 50, 36, 29, 32
]

def generateKeys(key):
    """Function to generate keys for different rounds of DES."""

    # Inititalizing variables required
    keys = []
    key = stringToBitArray(key)

    # Initial permutation on key
    key = permutation(key, keyPermutationMatrix1)

    # Split key in to (leftBlock->LEFT), (rightBlock->RIGHT)
    leftBlock, rightBlock = nSplit(key, 28)

    # 16 rounds of keys
    for i in range(16):
        # Do left shifting (different for different rounds)
        leftBlock, rightBlock = leftShift(leftBlock, rightBlock, SHIFT[i])
        # Merge them
        temp = leftBlock + rightBlock
        # Permutation on shifted key to get next key
        keys.append(permutation(temp, keyPermutationMatrix2))

    # Return generated keys
    return keys

# Sboxes used in the DES Algorithm
SboxesArray = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    ],

    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    ],

    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    ],

    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    ],

    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    ],

    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    ],

    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    ],

    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ]
]

def SboxSubstitution(bitArray):
    """Function to substitute all the bytes using Sbox."""

    # Split bit array into 6 sized chunks
    # For Sbox indexing
    blocks = nSplit(bitArray, 6)
    result = []

    for i in range(len(blocks)):
        block = blocks[i]
        # Row number to be obtained from first and last bit
        row = int( str(block[0]) + str(block[5]), 2 )
        # Getting column number from the 2,3,4,5 position bits
        column = int(''.join([str(x) for x in block[1:-1]]), 2)
        # Taking value from ith Sbox in ith round
        sboxValue = SboxesArray[i][row][column]
        # Convert the sbox value to binary
        binVal = binValue(sboxValue, 4)
        # Appending to result
        result += [int(bit) for bit in binVal]

    # Returning result
    return result


def addPadding(text):
    """Function to add padding according to PKCS5 standard."""

    # Determining padding length
    paddingLength = 8 - (len(text) % 8)
    # Adding paddingLength number of chr(paddingLength) to text
    text += chr(paddingLength) * paddingLength

    # Returning text
    return text

def removePadding(data):
    """Function to remove padding from plaintext according to PKCS5."""

    # Getting padding length
    paddingLength = ord(data[-1])

    # Returning data with removed padding
    return data[ : -paddingLength]

def expand(array, table):
    """Function to expand the array using table."""
    # Returning expanded result
    return [array[element - 1] for element in table]

def permutation(array, table):
    """Function to do permutation on the array using table."""
    # Returning permuted result
    return [array[element - 1] for element in table]

def leftShift(list1, list2, n):
    """Function to left shift the arrays by n."""
    # Left shifting the two arrays
    return list1[n:] + list1[:n], list2[n:] + list2[:n]

def nSplit(list, n):
    """Function to split a list into chunks of size n."""
    # Chunking and returning the array of chunks of size n
    # and last remainder
    return [ list[i : i + n] for i in range(0, len(list), n)]

def xor(list1, list2):
    """Function to return the XOR of two lists."""
    # Returning the xor of the two lists
    return [element1 ^ element2 for element1, element2 in zip(list1,list2)]

def binValue(val, bitSize):
    """Function to return the binary value as a string of given size."""

    binVal = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]

    # Appending with required number of zeros in front
    while len(binVal) < bitSize:
        binVal = "0" + binVal

    # Returning binary value
    return binVal

def stringToBitArray(text):
    """Funtion to convert a string into a list of bits."""

    # Initializing variable required
    bitArray = []
    for letter in text:
        # Getting binary (8-bit) value of letter
        binVal = binValue(letter, 8)
        # Making list of the bits
        binValArr = [int(x) for x in list(binVal)]
        # Apending the bits to array
        bitArray += binValArr

    # Returning answer
    return bitArray

def bitArrayToString(array):
    """Function to convert a list of bits to string."""

    # Chunking array of bits to 8 sized bytes
    byteChunks = nSplit(array, 8)
    # Initializing variables required
    stringBytesList = []
    stringResult = ''
    # For each byte
    for byte in byteChunks:
        bitsList = []
        for bit in byte:
            bitsList += str(bit)
        # Appending byte in string form to stringBytesList
        stringBytesList.append(''.join(bitsList))

    # Converting each stringByte to char (base 2 int conversion first)
    # and then concatenating
    result = ''.join([chr(int(stringByte, 2)) for stringByte in stringBytesList])

    # Returning result
    return result

if __name__ == '__main__':
    main()
