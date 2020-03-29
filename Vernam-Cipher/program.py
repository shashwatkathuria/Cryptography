# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 17:12:03 2020

@author: Shashwat Kathuria
"""

# Initializing variables required
errorMessage = "Error: Length of Key Must be >= Length of Plaintext"
mappingsDict = {}

def main():

    # Taking inputs from the user
    plaintext = input("Enter the plaintext : ")
    key = input("Enter the key (length should be >= length of plaintext) : ")

    # Initializing alphabets for rotating
    alphabets = "abcdefghijklmnopqrstuvwxyz"
    # Initializing values to alphabets
    for alphabet in alphabets.upper():
        mappingsDict[alphabet] = ord(alphabet) - 65

    plaintext = plaintext.upper()

    # Checking if key is invalid
    if len(key) <= len(plaintext):
        print(errorMessage)
    # Else applying algorithm
    else:
        # Encryption
        ciphertext = vernamEncryption(plaintext, key)

        # Decryption
        plaintext = vernamDecryption(ciphertext, key)

        # Printing answers
        print("Encrypted ciphertext is : ", ciphertext)
        print("Decrypted plaintext is  : ", plaintext)
    return

def vernamEncryption(plaintext, key):
    """Function to encrypt the plaintext using Vernam Encryption."""

    # Initializing ciphertext
    ciphertext = ''

    for i in range(len(plaintext)):
        ptLetter = plaintext[i]
        keyLetter = key[i]
        # Performing vernam encryption step
        sum = mappingsDict[ptLetter] + mappingsDict[keyLetter]
        # Subtracting 26 if sum overflows above values
        if sum >= 26:
            sum -= 26
        # Adding to ciphertext
        ciphertext += chr(sum + 65)

    # Returning ciphertext
    return ciphertext

def vernamDecryption(ciphertext, key):
    """Function to decrypt the ciphertext using Vernam Decryption."""

    # Initializing plaintext
    plaintext = ''

    for i in range(len(ciphertext)):
        ctLetter = ciphertext[i]
        keyLetter = key[i]
        # Performing vernam decryption step
        diff = mappingsDict[ctLetter] - mappingsDict[keyLetter]
        # Adding 26 if diff underflows above values
        if diff < 0:
            diff += 26
        # Adding to plaintext
        plaintext += chr(diff + 65)

    # Returning plaintext
    return plaintext

if __name__ == "__main__":
    main()
