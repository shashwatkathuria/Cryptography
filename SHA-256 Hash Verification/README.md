# SHA-256 HASH VERIFICATION
-----------------------------
INSTRUCTIONS TO RUN THE PROGRAM
-----------------------------

The following command must be executed to run the program:

          python3 SHA256HashVerification.

-----------------------------
ALGORITHM
-----------------------------

In SHA-256 Hash Verification we need to compute the first hash
h0 on a file and verify the same with the answer given and compute
the hash h0 for the target file. The hashing is done as follows: first,
the last block which is irregular in size is hashed and then its hashed
value is concatenated to the end of the previous block. Then, a hash of
the concatenated previous block is computed and concatenated to its
previous block and so on until we get the hashed value h0 of the first
block. When files are opened, to verify that the contents are correct and
not tampered, the file reader checks whether the hash of the first concatenated
block is equal to h0, if yes, then it moves on to the second block and checks
whether the hash of the second block is equal to the latter concatenated value
of the first block and so on keeps verifying whether or not the file or
message is tampered. The reason for hashing blocks and not the whole file is
that while streaming videos or any other data online, we get sizable blocks
and not the whole file, because otherwise loading would take a long time.

-----------------------------
