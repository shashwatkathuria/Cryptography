# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 17:12:03 2020

@author: Shashwat Kathuria
"""

errorMessage = "Error: Length of Key Must be >= Length of Plaintext"
mappingsDict = {}

def main():
    plaintext = input("Enter the plaintext : ")
    key = input("Enter the key (length should be >= length of plaintext) : ")

    alphabets = "abcdefghijklmnopqrstuvwxyz"
    for alphabet in alphabets.upper():
        mappingsDict[alphabet] = ord(alphabet) - 65

    plaintext = plaintext.upper()

    if len(key) != len(plaintext):
        print(errorMessage)
    else:
        ciphertext = vernamEncryption(plaintext, key)
        plaintext = vernamDecryption(ciphertext, key)
        print("Encrypted ciphertext is : ", ciphertext)
        print("Decrypted plaintext is  : ", plaintext)
    return

def vernamEncryption(plaintext, key):
    ciphertext = ''
    for i in range(len(plaintext)):
        ptLetter = plaintext[i]
        keyLetter = key[i]
        sum = mappingsDict[ptLetter] + mappingsDict[keyLetter]
        if sum >= 26:
            sum -= 26
        ciphertext += chr(sum + 65)
    return ciphertext

def vernamDecryption(ciphertext, key):
    plaintext = ''
    for i in range(len(ciphertext)):
        ctLetter = ciphertext[i]
        keyLetter = key[i]
        diff = mappingsDict[ctLetter] - mappingsDict[keyLetter]
        if diff < 0:
            diff += 26
        plaintext += chr(diff + 65)
    return plaintext


if __name__ == "__main__":
    main()
