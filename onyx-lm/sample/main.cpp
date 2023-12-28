#include <iostream>
#include <string>

#include "onyx.h"

int main() {
    onyx::InitOnyx("http://localhost:8585");
    std::string login, password;

    // Запрашиваем логин и пароль у пользователя
    std::cout << "Login: ";
    std::getline(std::cin, login);
    std::cout << "Password: ";
    std::getline(std::cin, password);

    // Проверяем логин и пароль
    while (!onyx::Auth(login.c_str(), password.c_str())) {
        std::cout << "Wrong login or password. Retry" << std::endl;
        std::cout << "Login: ";
        std::getline(std::cin, login);
        std::cout << "Password: ";
        std::getline(std::cin, password);
    }

    // Если логин и пароль верны, запускаем бесконечный цикл эхо программы
    std::cout << "Successfull login" << std::endl;
    while (true) {
        std::string input;
        std::cout << "> ";
        std::getline(std::cin, input);
        std::cout << "Your message: " << input << std::endl;
    }
    return 0;
}