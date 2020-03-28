# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 16:25:38 2020

@author: Shashwat Kathuria
"""

def main():
    plaintext = input('Enter the message to be encrypted : ')
    key = int(input('Enter the key (a number) : '))
    ciphertext = caesarEncryption(plaintext, key)
    plaintext = caesarDecryption(ciphertext, key)
    print("Encrypted ciphertext is : ", ciphertext)
    print("Decrypted plaintext is  : ", plaintext)
    return

def caesarEncryption(plaintext, key):
    """Function to encrypt the plaintext using Caesar Encryption."""
    ciphertext = ''
    for letter in plaintext:
        ascii = ord(letter)
        if letter.isalpha():
            temp = ascii + key
            if (temp > 90 and letter.isupper()) or (temp > 122 and letter.islower()):
                ciphertext += chr(temp - 26)
            else:
                ciphertext += chr(temp)

    return ciphertext

def caesarDecryption(ciphertext, key):
    """Function to decrypt the ciphertext using Caesar Decryption."""
    plaintext = ''
    for letter in ciphertext:
        ascii = ord(letter)
        if letter.isalpha():
            temp = ascii - key
            if ( (temp < 65 and letter.isupper()) or (temp < 97 and letter.islower()) ):
                plaintext += chr(temp + 26)
            else:
                plaintext += chr(temp)

    return plaintext

if __name__ == "__main__":
    main()
