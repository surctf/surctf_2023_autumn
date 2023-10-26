#include <stdio.h>
#include <stdlib.h>

void win(void) {
    puts("Congratulations, you have passed the test of the Lottery Ball!");
    system("/bin/sh");
}

int main(void) {
    char inp[256];
    uint number;
    number = 0x13371337;
    puts("The Lottery Ball will grant access to the treasure chest if you bravely pass the challenge!");
    fflush(stdout);
    fputs("Enter your ticket number: ", stdout);
    fflush(stdout);
    scanf("%s", inp);
    if (number == 0xDEFEC8ED) {
        win();
        fflush(stdout);
    } else {
        puts("No luck for you today!");
        fflush(stdout);
    }
    exit(0);
}


