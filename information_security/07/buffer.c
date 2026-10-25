#include <stdio.h>
#include <string.h>

void secret(void) {
    printf("You have entered the secret function!\n");
}

void useInput(char* input) {
    char buffer[30];
    strcpy(buffer, input);
    printf(buffer); //print input to user for validation
    // do some stuff
}

int main(int argc, char* argv[]) {
    useInput(argv[1]);
    return 0;
}