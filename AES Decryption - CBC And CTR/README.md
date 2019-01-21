# AES DECRYPTION - CBC AND CTR MODE
---------------------------------------
INSTRUCTIONS TO RUN THE PROGRAM
---------------------------------------

The following command must be executed to run the program:


            python3 AESCbcAndCtr.py

---------------------------------------
ALGORITHM
---------------------------------------

In the AES Decryption of CBC and CTR Mode, the key and
ciphertext together alongwith the respective algorithms and
implementations of the modes are used to decrypt the message.

In the CBC Mode, the IV is first encrypted and then xored with
the first block of the plaintext and then encrypted using AES
which forms the first block of the ciphertext and that value also
acts like the IV for the second block and so on until all the
ciphertext is encrypted. Decrytion is done in the reverse order
of these steps and is quite straight forward. This mode is
sequential unlike CTR Mode.

In the CTR Mode, the IV sent as the first block of the ciphertext.
Using IV, then a counter increments the value of IV by the block
number which is then encrypted using AES. The result of this AES is
xored with the corresponding plaintext block which makes up the
ciphertext block. Decrytion is done in the reverse order of these
steps and is quite staright forward. This mode is parallelizable
unlike CBC Mode.
---------------------------------------
