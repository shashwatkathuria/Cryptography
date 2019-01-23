# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 19:17:22 2019

@author: Shashwat Kathuria
"""
import urllib2

blockSize = 16

ciphertext = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'
targetUrl = 'http://crypto-class.appspot.com/po?er='

def main():
    paddingOracle = PaddingOracle()
    paddingOracle.decrypt(ciphertext)
    plaintext = paddingOracle.getPlaintext()
    print(plaintext)


class PaddingOracle():


    def __init__(self):
        print('PaddingOracle initializing...')
        self.ciphertext = ''
        self.plaintext = ''
        self.padding = 0
        self.blockSize = blockSize
        self.hexBlockSize = blockSize * 2
        self.noOfBlocks = 0
        self.guessLowerBound = 1
        self.guessUpperBound = 256

    def getPlaintext(self):
        return self.plaintext[:(self.blockSize * self.noOfBlocks) - self.padding]

    def decrypt(self, cipher):
        print('hacking...')
        self.ciphertext = cipher
        self.noOfBlocks = len(self.ciphertext) / self.hexBlockSize
        # Removing IV Block
        self.plaintext = bytearray(self.blockSize * (self.noOfBlocks - 1))

        # No need to decrypt the IV
        for i in range(0, self.noOfBlocks - 1):
            self.blockGuess(self.noOfBlocks - i)


    def blockGuess(self, iBlocks):

        padding = 0

        for i in range(0, self.blockSize):

            if i < padding:
                continue

            guess_index = self.blockSize * (iBlocks - 1) - 1 - i
            print('decrypting cipher character No. ' + str(guess_index) + ': '),
            # Plain text is byte array but cipher text is hex array so the size ratio is 1:2
            guess_index *= 2

            query_trail = ''

            for iTrail in range(1, i + 1):
                pt_index = self.plaintext[guess_index / 2 + iTrail]
                ct_index = self.ciphertext[guess_index + iTrail * 2:guess_index + iTrail * 2 + 2]
                mask = format(pt_index ^ (i + 1) ^ int(ct_index, 16), '02x')
                query_trail += mask

            for guess in range(self.guessLowerBound, self.guessUpperBound):
                if 0 == guess % 32:
                    print('\n.'),
                else:
                    print('.'),

                query = self.ciphertext[:guess_index]

                ct_index = self.ciphertext[guess_index:guess_index + 2]
                mask = format(guess ^ (i + 1) ^ int(ct_index, 16), '02x')
                query += mask

                query += query_trail
                query += self.ciphertext[self.hexBlockSize * (iBlocks - 1):self.hexBlockSize * iBlocks]

                if self.sendQuery(query):
                    if i != 0 or iBlocks != self.noOfBlocks:
                        print('Found!')
                        self.plaintext[guess_index / 2] = chr(guess)
                    else:
                        print('Found real padding: ' + str(guess))
                        self.plaintext[guess_index / 2] = chr(guess)
                        for iPadding in range(guess_index / 2 - 1, guess_index / 2 - guess, -1):
                            print('decrypting cipher character No. ' + str(iPadding) + ': real padding!')
                            self.plaintext[iPadding] = chr(guess)
                        self.padding = padding = guess
                        self.guessLowerBound = 32
                        # Chars between 32~127 are printable in ASCII table.
                        self.guessUpperBound = 128
                    print self.plaintext
                    break

                if self.guessUpperBound == guess:
                    print('NOT found!')
                    print('Check your code, there must be something wrong...')
                    return


    def sendQuery(self, query):

        target = targetUrl + urllib2.quote(query)
        req = urllib2.Request(target)

        try:
            urllib2.urlopen(req)

        except urllib2.HTTPError, e:
            if e.code == 404:
                return True
            return False


if __name__ == "__main__":
    main()
