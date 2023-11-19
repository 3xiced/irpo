#include "onyx.h"

#include <iostream>

#include "cpr/cpr.h"

namespace onyx {
void Onyx::get_system_info() noexcept {}

void Onyx::validate_access() noexcept {}

void Onyx::auth(const std::string& login, const std::string& password) {
    auto r = cpr::Get(cpr::Url{"http://yandex.ru"},
                      cpr::Header{{"Content-Type", "application/json"}});
    std::cout << r.status_code;
}
}  // namespace onyx
