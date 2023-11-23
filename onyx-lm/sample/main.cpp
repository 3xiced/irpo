#include <iostream>
#include <string>

#include "onyx.h"

int main() {
    onyx::InitOnyx("http://localhost:8585");

    if (onyx::Auth("3xiced", "1q2wazsx")) {
        while (true) {
            std::string msg;
            std::cout << "Type message: ";
            std::cin >> msg;
            std::cout << std::endl << "Your message: " << msg;
            if (msg == "bye") return 0;
        }
    }
    return 0;
}