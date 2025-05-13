#include <cstdio>
#include <cstdlib>
#include <string>
#include <unistd.h>

int main(int argc, char** argv) {
    char *args[] = {"/usr/bin/python3", "/boot/BOOTMGR.py", nullptr};
    execvp(args[0], args);
    return 0;
};