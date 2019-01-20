# MANY TIME PASS HACK
------------------------
INSTRUCTIONS TO RUN THE PROGRAM
------------------------

The following command must be executed to run the program:

      python3 manytimepass.py

------------------------
ALGORITHM
------------------------

In Many Time Pass Hack, we exploit the properties of
xor. When messages m1 and m2 are encrypted using the
same one time pass key, we get a relation which relates
the ciphertext c1 and c2 with the messages, verbosely,

        c1 xor c2 = (m1 xor key) xor (m2 xor key)
        c1 xor c2 = m1 xor m2

It turns out that English language and ASCII encoding
has enough redundancy to decode the ciphertexts. That is,
whenever we encounter the xor of a space ' ' and a character
we get the same character with inverted case. So this implies
that whenever there is a space in m1 and m2 and not in the
other, we can get the original alphabet with inverted case.
We carry this on for all the strings and in the last apply a
guessing heuristic to get the result based on maximum
occurences of the possibilities. If we encounter the xor of
a weird punctuation mark with a space or something else, we get
inconsistent letters which can be seen as having many different
alphabets in the same possibility position. If we get such
possibilities or occurences spanned over more than one letter,
then they are probably a weird punctuation mark or a number
else it is a space.

------------------------        
