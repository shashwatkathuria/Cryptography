# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 16:25:38 2020

@author: Shashwat Kathuria
"""

def main():

    print()
    # Taking inputs from the user
    plaintext = input('Enter the message to be encrypted : ')
    key = int(input('Enter the key (a number) : '))
    print()

    # Encryption
    ciphertext = caesarEncryption(plaintext, key)

    # Decryption
    plaintext = caesarDecryption(ciphertext, key)

    # Printing answers
    print()
    print("Encrypted ciphertext is : ", ciphertext)
    print("Decrypted plaintext is  : ", plaintext)
    print()
    return

def caesarEncryption(plaintext, key):
    """Function to encrypt the plaintext using Caesar Encryption."""

    # Initializing ciphertext
    ciphertext = ''

    for letter in plaintext:
        ascii = ord(letter)
        # If the letter is an alphabet
        if letter.isalpha():
            # Rotating key number of times in alphabet order
            temp = ascii + key
            # If it overflows, subtract 26 and then add to ciphertext
            if (temp > 90 and letter.isupper()) or (temp > 122 and letter.islower()):
                ciphertext += chr(temp - 26)
            # Else just add to ciphertext
            else:
                ciphertext += chr(temp)

    # Returning ciphertext
    return ciphertext

def caesarDecryption(ciphertext, key):
    """Function to decrypt the ciphertext using Caesar Decryption."""

    # Initializing plaintext
    plaintext = ''

    for letter in ciphertext:
        ascii = ord(letter)
        # If the letter is an alphabet
        if letter.isalpha():
            # Reverse rotating key number of times in alphabet order
            temp = ascii - key
            # If it underflows, add 26 and then add to plaintext
            if ( (temp < 65 and letter.isupper()) or (temp < 97 and letter.islower()) ):
                plaintext += chr(temp + 26)
            # Else just add to plaintext
            else:
                plaintext += chr(temp)

    # Returning plaintext
    return plaintext

if __name__ == "__main__":
    main()
