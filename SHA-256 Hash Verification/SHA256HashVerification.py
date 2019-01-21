# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 12:29:45 2019

@author: Shashwat Kathuria
"""

# SHA-256 HASH VERIFICATION

import os, codecs
from Crypto.Hash import SHA256

def main():
    blockSize = 1024
    checkFile = "check.mp4"
    verifyHash = "03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8"
    print("\nThe last hash (h0) to be checked for file " + checkFile + " is: " + verifyHash)
    targetFile = "target.mp4"
    checkHash = computeLastHashh0(checkFile, blockSize)
    targetHash = computeLastHashh0(targetFile, blockSize)
    print("\nRESULTS : \n")
    if checkHash == verifyHash:
        print("\nThe last hash (h0) to be checked for file " + checkFile + " is correct.")
    print("The last hash (h0) of MP4 File " + checkFile + " is : " + checkHash + "\n")
    print("The last hash (h0) of MP4 File " + targetFile + " is : " + targetHash + "\n")


def computeLastHashh0(filePath, blockSize):

    fileSize = os.path.getsize(filePath)
    file = open(filePath, "rb")
    lastHash = ""

    for blockData in readBlocksFromEnd(file, fileSize, blockSize):
        SHA256Engine = SHA256.new()
        SHA256Engine.update(blockData)

        if lastHash != "":
            SHA256Engine.update(lastHash)

        lastHash = SHA256Engine.digest()

    lastHash = codecs.encode(lastHash, 'hex')
    lastHash = codecs.decode(lastHash, 'utf-8')
    return lastHash

def readBlocksFromEnd(file, fileSize, blockSize):
    blockNumberFromEnd = 0
    lastBlockSize = fileSize % blockSize
    lastPosition = fileSize
    readEndPosition = lastPosition

    while readEndPosition > 0:

        if (blockNumberFromEnd == 0):
            size = lastBlockSize
        else:
            size = blockSize

        readStartPosition = readEndPosition - size
        file.seek(readStartPosition)

        data = file.read(blockSize)
        blockNumberFromEnd += 1
        readEndPosition -= size

        yield data


if __name__ == "__main__":
    main()
