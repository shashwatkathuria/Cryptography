#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <crypt.h>

int checkPossibilities(char *hash, int psize);

int main(int argc, string argv[])
{
    //checks if the contraints are satisfied
    if (argc != 2)
    {
        printf("Usage:./crack ");
    }

    int found = 1;
    //iterates through lengths of passwords
    for (int i = 1; i <= 4; i++)
    {
        //checks the possiilities
        found = checkPossibilities(argv[1], i);
        if (found == 0)
        {
            break;
        }
    }
    //returns 0 if no password found
    return 0;
}


int checkPossibilities(char *hash, int psize)
{

    char *possibilities = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

    char *cryptans = NULL;
    //allocates memory for salt
    char *salt = malloc((2 + 1) * sizeof(char));
    strncpy(salt, hash, 2);
    salt[2] = '\0';

    int nw = 1, ne = 1, nr = 1;
    //limit the number of permutations according to password length
    if (psize == 4)
    {
        nw = ne = nr = 52;
    }
    else if (psize == 3)
    {
        ne = nr = 52;
    }
    else if (psize == 2)
    {
        nr = 52;
    }

    //allocates memory for password according to length
    char *password = malloc((psize + 1) * sizeof(char));
    password[psize] = '\0';
    //loops through the possible permutations
    for (int w = 0; w < nw; w++)
    {
        if (nw == 52)
        {
            password[psize - 4] = possibilities[w];
        }
        for (int e = 0; e < ne; e++)
        {
            if (ne == 52)
            {
                password[psize - 3] = possibilities[e];
            }
            for (int r = 0; r < nr; r++)
            {
                if (nr == 52)
                {
                    password[psize - 2] = possibilities[r];
                }
                for (int q = 0; q < 52; q++)
                {
                    password[psize - 1] = possibilities[q];
                    cryptans = crypt(password, salt);
                    if (strcmp(cryptans, hash) == 0)
                    {
                        //outputs answer if any
                        printf("\nYour password is %s\n", password);
                        return 0;
                    }
                }
            }
        }
    }

    return 1;
}