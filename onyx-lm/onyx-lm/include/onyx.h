#pragma once

#include "onyx_export.h"

namespace onyx {
// Функция auth выбирает случайный из созданных onyx'ов, логинится через него.
// В случае успешной авторизации, запускается в том же потоке (отдельном) функция которая в
// течение 1 минуты установит has_access{true} у всех объектов в случайном порядке. В том же
// потоке через случайное время от минуты до 10 минут проверится, везде ли установлен флаг
// true. Если гдето нет - запрос на бан по железу, abort();
void ONYX_EXPORT InitOnyx(const char* onyx_server_addr);
bool ONYX_EXPORT Auth(const char* login, const char* password);
}  // namespace onyx