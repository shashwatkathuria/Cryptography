# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 12:29:45 2019

@author: Shashwat Kathuria
"""

# SHA-256 HASH VERIFICATION

import os, codecs
from Crypto.Hash import SHA256

def main():

    # Declaring block size in number of bits
    blockSize = 1024

    # Declaring input files information
    checkFile = "check.mp4"
    verifyHash = "03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8"
    print("\nThe last hash (h0) to be checked for file " + checkFile + " is: " + verifyHash)
    targetFile = "target.mp4"

    # Calling funaction to compute last hash on both the video files
    checkHash = computeLastHashh0(checkFile, blockSize)
    targetHash = computeLastHashh0(targetFile, blockSize)

    # Printing the result
    print("\nRESULTS : \n")

    # Checking if the procedure we applied is correct by
    # verifying one hash answer already givem
    if checkHash == verifyHash:
        print("\nThe last hash (h0) to be checked for file " + checkFile + " is correct.")
    print("The last hash (h0) of MP4 File " + checkFile + " is : " + checkHash + "\n")

    # Printing the target hash answer
    print("The last hash (h0) of MP4 File " + targetFile + " is : " + targetHash + "\n")


def computeLastHashh0(filePath, blockSize):
    """Funtion to compute the last hash of a file using SHA-256. Inputs are the file
       and the block size."""

    lastHash = ""

    # Computing hash starting from the last block which might
    # or might not be less than blocksize
    for blockData in readBlocksFromEnd(filePath, blockSize):

        # Declaring new SHA-256 Engine (to be done every time a new data is to be hashed)
        SHA256Engine = SHA256.new()

        # For every block other than the last one
        if lastHash != "":
            # Updating the contents to be hashed. Two calls are equal to concatenated one call of the function.
            SHA256Engine.update(blockData)
            SHA256Engine.update(lastHash)

        # For last block
        else:
            # Updating the contents to be hashed. In the starting no hash is there for last block
            SHA256Engine.update(blockData)

        # Getting the value of hash in bytes
        lastHash = SHA256Engine.digest()

    # Encoding the last hash using hex coding and then decoding using utf-8 codec
    # to give output in same format as input

    lastHash = codecs.encode(lastHash, 'hex')
    lastHash = codecs.decode(lastHash, 'utf-8')

    return lastHash

def readBlocksFromEnd(filePath, blockSize):
    """Generator function to get the blocks of information one at a time from the
       file to be read in bytes. Inputs are the file path and the block size."""

    # Getting and storing the size of the input file
    fileSize = os.path.getsize(filePath)

    # Opening the file to read in byte mode as the file
    # is written in bytes
    file = open(filePath, "rb")

    # Parameters necessary for reading from file
    blockNumberFromEnd = 0
    lastBlockSize = fileSize % blockSize
    lastPosition = fileSize
    readEndPosition = lastPosition

    # Reading file block by block starting from end block
    while readEndPosition > 0:

        # Because the length of the last block may be smaller than block size
        if (blockNumberFromEnd == 0):
            size = lastBlockSize
        else:
            size = blockSize

        # Reading from file by updating pointer to start of block required
        readStartPosition = readEndPosition - size
        file.seek(readStartPosition)
        data = file.read(blockSize)

        # Updating parameters
        blockNumberFromEnd += 1
        readEndPosition -= size

        # Generating data block by block inn byte form
        yield data


if __name__ == "__main__":
    main()
