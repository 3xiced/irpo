#pragma once

#include <string>
#include <vector>

#include "onyx_export.h"

namespace onyx {
namespace impl {
static const int __real {(rand() % 10) + 1};
static std::vector<onyx::Onyx*> __onyxes;
}  // namespace impl
class ONYX_EXPORT Onyx {
    bool has_access{false};
    /// <summary>
    /// Используется для получения информации о системе для привязки по железу
    /// </summary>
    static std::string GetSystemInfo() noexcept;
    /// <summary>
    /// Случайно во времени проверяет, валиден ли пользователь, если нет - блокирует
    /// устройство на сервере по железу
    /// </summary>
    void ValidateAccess() noexcept;

   public:
    /// <summary>
    /// Основная функция класса. Передается логин, пароль, функция проверяет
    /// пользователя на сервере и в случае не успешной авторизации генерирует исключение.
    /// </summary>
    /// <param name="login"></param>
    /// <param name="password"></param>
    /// <returns></returns>
    void Auth(const std::string& login, const std::string& password);
};

// Функция auth выбирает случайный из созданных onyx'ов, логинится через него.
// В случае успешной авторизации, запускается в том же потоке (отдельном) функция которая в
// течение 1 минуты установит has_access{true} у всех объектов в случайном порядке. В том же
// потоке через случайное время от минуты до 10 минут проверится, везде ли установлен флаг
// true. Если гдето нет - запрос на бан по железу, abort();

void ONYX_EXPORT InitOnyx() {
    int onyxes{(rand() % 10) + 1};
    for (int i = 0; i < onyxes; i++) impl::__onyxes.push_back(new Onyx);
}

bool ONYX_EXPORT Auth(const char* login, const char* password) {
    Onyx* _onyx = impl::__onyxes.at(impl::__real);
    _onyx->Auth(login, password);
}

}  // namespace onyx