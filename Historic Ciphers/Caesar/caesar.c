#include<stdio.h>
#include<cs50.h>
#include<string.h>

int main(int argc, string argv[])
{
    int k;
    //takes the command line argument representing the key
    if (argc == 2)
    {
        k = atoi(argv[1]);
        k = k % 26;
    }
    //Warns user if the command line argument doesn't satisfy the requirements
    else
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }
    //prompts the user for plaintext
    char *s = get_string("\nplaintext: ");

    //calculates the ciphertext
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if ((s[i] >= 65 && s[i] <= 90) || (s[i] >= 97 && s[i] <= 122))
        {
            if ((s[i] + k) > 90 && s[i] <= 90)
            {
                s[i] += -26 + k;
            }
            else if ((s[i] + k) > 122 && s[i] <= 122)
            {
                s[i] += -26 + k;
            }
            else
            {
                s[i] += k;
            }
        }

    }
    //displays the ciphertext
    printf("ciphertext: %s\n", s);
    return 0;
}