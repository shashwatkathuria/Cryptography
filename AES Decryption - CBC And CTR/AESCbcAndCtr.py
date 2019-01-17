# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 19:39:35 2019

@author: Shashwat Kathuria
"""

import sys
from operator import methodcaller
import re
import numpy
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random
import codecs

def main():
    blockSize = 16
    cbcKey = "140b41b22a29beb4061bda66b6747e14"
    ctrKey = "36f18357be4dbd77f050515c73fcf9f2"
    cbcMessage1 = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"
    cbcMessage2 = "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"
    ctrMessage1 = "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"
    ctrMessage2 = "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"
    
    print(cbcDecryption(cbcKey, cbcMessage1, blockSize))
    print(ctrDecryption(cbcKey, ctrMessage2, blockSize))
    
def ctrDecryption(ctrKey, ctrMessage, blockSize):
        key = codecs.decode(ctrKey, 'hex')
        ciphertextAndIV = codecs.decode(ctrMessage, 'hex')
        IV = ciphertextAndIV[:blockSize]
        ciphertext = ciphertextAndIV[blockSize:]
        ctr = Counter.new(blockSize * 8, initial_value = int(codecs.encode(IV, "hex"),16))
        aesEngine = AES.new( key , AES.MODE_CTR,counter = ctr)
        paddedStr = aesEngine.decrypt(ciphertext)
        return paddedStr


def cbcDecryption(cbcKey, cbcMessage, blockSize):
	key = codecs.decode(cbcKey, 'hex')
	ciphertextAndIV = codecs.decode(cbcMessage, 'hex')
	IV = ciphertextAndIV[:blockSize]
	ciphertext = ciphertextAndIV[blockSize:]
	aesEngine = AES.new(key,AES.MODE_CBC,IV)
	paddedStr = aesEngine.decrypt(ciphertext)
	paddingAmount = ord(paddedStr[len(paddedStr)-1:])
	return paddedStr[:-paddingAmount]
if __name__ == "__main__":
    main()
    