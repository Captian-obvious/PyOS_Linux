#include <iostream>
#include <unistd.h>
#include <string>
#include <cstring>

void print_err(std::string output) {
    std::cout << "\033[1;31mPyBoot: " << output << "\033[0m" << std::endl; // red
};

void print_warn(std::string output) {
    std::cout << "\033[1;33mPyBoot: " << output << "\033[0m" << std::endl; // yellow
};
int main(int argc, char** argv) {
    const char *envPath = "/usr/bin/env";
    const char *pythonCmd = "python";
    const char *scriptPath = "./BOOTMGR.py";
    bool debugMode = false;
    // Check for "--debug" argument
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--debug") == 0) {
            debugMode = true;
            break;
        };
    };
    // Verify BOOTMGR.py exists
    if (access(scriptPath, F_OK) != 0) {
        print_err("BOOTMGR.py not found!");
        return 1;
    };
    // Construct arguments
     char *args[] = {const_cast<char*>(envPath), const_cast<char*>(pythonCmd), const_cast<char*>(scriptPath), nullptr};
    if (debugMode) {
        args[3] = const_cast<char*>("--debug");
        args[4] = nullptr;
        print_warn("Debug mode is enabled, this is not recommended for production use. (--debug)");
    };
    execvp(args[0], args);
    print_err("Failed to run bootloader!");
    return 1;
};