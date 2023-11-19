#pragma once

#include <string>

#include "onyx_export.h"

namespace onyx {
class ONYX_EXPORT Onyx {
    bool has_access{false};
    /// <summary>
    /// Используется для получения информации о системе для привязки по железу
    /// </summary>
    static void get_system_info() noexcept;
    /// <summary>
    /// Случайно во времени проверяет, валиден ли пользователь, если нет - блокирует
    /// устройство на сервере по железу
    /// </summary>
    void validate_access() noexcept;

   public:
    /// <summary>
    /// Основная функция класса. Передается логин, пароль, функция проверяет
    /// пользователя на сервере и в случае не успешной авторизации генерирует исключение.
    /// </summary>
    /// <param name="login"></param>
    /// <param name="password"></param>
    /// <returns></returns>
    void auth(const std::string& login, const std::string& password);
};
}  // namespace onyx