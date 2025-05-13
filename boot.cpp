#include <iostream>
#include <unistd.h>
#include <string>
#include <cerrno>
#include <cstring>
// Main and helper functions
// This is a simple bootloader that runs a Python script (BOOTMGR.py) using the system's Python interpreter.
void print_err(std::string output) {
    std::cout << "\033[1;31mPyBoot: " << output << "\033[0m" << std::endl; // red
};
void print_info(std::string output) {
    std::cout << "PyBoot: " << output << std::endl; // normal
};
void print_warn(std::string output) {
    std::cout << "\033[1;33mPyBoot: " << output << "\033[0m" << std::endl; // yellow
};
// Where the magic happens
// This function is the entry point of the bootloader. It checks for the existence of the BOOTMGR.py script,
// constructs the command to run it using the system's Python interpreter, and executes it.
// It also handles the "--debug" argument to enable debug mode.
// If the "--recover" argument is passed, it enters recovery mode instead.
// The recovery mode is not implemented yet, but a placeholder is provided for future development.
int main(int argc, char** argv) {
    const char *envPath = "/usr/bin/env";
    const char *pythonCmd = "python";
    const char *scriptPath = "./BOOTMGR.py";
    bool debugMode = false;
    bool recoveryMode = false;
    // Check for "--recovery" argument
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--recovery") == 0) {
            recoveryMode = true;
            break;
        };
    };
    // Check for "--debug" argument
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--debug") == 0) {
            debugMode = true;
            break;
        };
    };
    if (!recoveryMode){
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
        print_err("Failed to run bootloader! Error: " + std::string(strerror(errno)));
        return 1;
    }else{
        // Recovery mode
        print_warn("Entering recovery setup (--recovery)");
        __recovery_ui();
        return 0;
    };
};

void __recovery_ui(){
    print_info("Loading recovery mode...");
    // TODO: Add recovery mode code here
    print_warn("Recovery mode is not (fully) implemented yet.");
    return;
};