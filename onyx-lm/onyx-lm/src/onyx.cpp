#include "onyx.h"

#include <iostream>

#include "SMBIOS.h"
#include "cpr/cpr.h"

namespace onyx {

std::string Onyx::GetSystemInfo() noexcept {
    InitSMBIOS();
    return BaseBoardSerial;
}

void Onyx::ValidateAccess() noexcept {}

void Onyx::Auth(const std::string& login, const std::string& password) {
    // auto r = cpr::Get(cpr::Url{"http://yandex.ru"},
    //   cpr::Header{{"Content-Type", "application/json"}});
    // std::cout << r.status_code;
    auto device_sn = GetSystemInfo();
    std::cout << device_sn << std::endl;
}
}  // namespace onyx
