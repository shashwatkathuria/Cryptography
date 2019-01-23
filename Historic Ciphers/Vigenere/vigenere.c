#include<stdio.h>
#include<cs50.h>
#include<string.h>
#include<ctype.h>

int main(int argc, string argv[])
{
    int *k = NULL;
    //warns user if the requirements are not satisfied
    if (argc != 2)
    {
        printf("Usage: ./vigenere k\n");
        return 1;
    }
    //writes necessary offsets to an array
    else
    {
        //checks if all the characters are alphabets
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (isalpha(argv[1][i]) == 0)
            {
                printf("Usage: ./vigenere k\n");
                return 1;
            }
        }
        k = malloc(strlen(argv[1]) * sizeof(int));
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            k[i] = toupper(argv[1][i]);
            k[i] -= 65;
        }
    }

    //prompts user for plaintext
    string s = get_string("plaintext: ");
    //calculates ciphertext
    for (int i = 0, n = strlen(s), j = 0; i < n; i++, j++)
    {
        if (isalpha(s[i]) != 0)
        {
            //checks if letter exceeds the ascii limits and does the necessary calculations
            int flag1 = 0;
            int y = s[i];
            int x = y;
            j = j % (strlen(argv[1]));
            if (isupper(s[i]) == 0)
            {
                flag1 = 1;
            }
            x += (k[j] % 26);
            if (x > 122)
            {
                x -= 26;
            }

            else if (y <= 90 && x > 90)
            {
                x -= 26;
            }
            s[i] = x;
        }
        else
        {
            j--;
        }
    }
    //outputs the ciphertext on the screen
    printf("ciphertext: %s\n", s);
}