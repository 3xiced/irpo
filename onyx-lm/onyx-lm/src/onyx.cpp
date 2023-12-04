#include "onyx.h"

#include <iostream>
#include <random>
#include <string>
#include <thread>
#include <vector>

#include "SMBIOS.h"
#include "cpr/cpr.h"
#include "exceptions.h"
#include "nlohmann/json.hpp"

namespace onyx {
namespace impl {
using json = nlohmann::json;
class Onyx final {
    bool has_access_{false};
    /// <summary>
    /// Используется для получения информации о системе для привязки по железу
    /// </summary>
    static std::string GetSystemInfo() noexcept;

   public:
    /// <summary>
    /// Основная функция класса. Передается логин, пароль, функция проверяет
    /// пользователя на сервере и в случае не успешной авторизации генерирует исключение.
    /// </summary>
    /// <param name="login"></param>
    /// <param name="password"></param>
    /// <returns></returns>
    void Auth(const std::string& login, const std::string& password) const;
    void Block() const;
    void SetOk();
    bool has_access() const noexcept;
};

// Utils and variables
static std::vector<Onyx*> __onyxes;
static std::string __onyx_server_addr;

inline void SetAllTrue() {
    static std::random_device rd;   // obtain a random number from hardware
    static std::mt19937 gen(rd());  // seed the generator
    static std::uniform_int_distribution<> distr(15, 90);  // define the range
    std::cout << "Looping over " << __onyxes.size() << " onyxes..." << std::endl;
    for (auto _onyx : __onyxes) {
        auto sleep_time = distr(gen);
        std::cout << "Current _onyx: " << &_onyx << ", sleeping for " << sleep_time
                  << " seconds..." << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(sleep_time));
        _onyx->SetOk();
        std::cout << "_onyx: " << &_onyx << " setOk" << std::endl;
    }

    int sleep_time = distr(gen) * 3.34;
    std::cout << "All onyxes active, sleeping for " << sleep_time
              << " seconds before running validator..." << std::endl;
    // В случайное время от 49,5 секунд до 300 запускается валидатор
    std::this_thread::sleep_for(std::chrono::seconds(sleep_time));
    for (Onyx* _onyx : __onyxes)
        if (!_onyx->has_access()) _onyx->Block();
}

// Onyx
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void Onyx::Auth(const std::string& login, const std::string& password) const {
    auto device_sn = GetSystemInfo();
    json request_payload = {
        {"login", login}, {"password", password}, {"device_sn", device_sn}};
    std::cout << "Attempt logging in for user='" << login << "' password='" << password
              << "' device_sn='" << device_sn << "'" << std::endl
              << "request_payload='" << request_payload << "'" << std::endl;
    cpr::Response r = cpr::Post(cpr::Url{__onyx_server_addr + "/api/user/auth"},
                                cpr::Body{request_payload.dump()},
                                cpr::Header{{"Content-Type", "application/json"}});
    std::cout << "Response status code from /api/user/auth: " << r.status_code << std::endl;
    switch (r.status_code) {
        case 204: {
            std::cout << "Creating SetAllTrue thread..." << std::endl;
            std::thread runner(SetAllTrue);
            runner.detach();
            std::cout << "SetAllTrue thread detached" << std::endl;
            break;
        }
        case 409:
            throw ::onyx::exceptions::AlreadyLoggedIn();
        case 403:
            throw ::onyx::exceptions::Blocked();
        case 404:
        case 400:
            throw ::onyx::exceptions::BadCredentials();
        default:
            throw std::runtime_error("internal error");
    }
}

std::string Onyx::GetSystemInfo() noexcept { return BaseBoardSerial; }

void Onyx::Block() const {
    auto device_sn = GetSystemInfo();
    std::cout << "Onyx " << &*this << " invalid, sending block request..." << std::endl;
    cpr::Response r = cpr::Post(cpr::Url{__onyx_server_addr + "/api/user/block"},
                                cpr::Payload{{"device_sn", device_sn}});
    std::cout << "/api/user/block response status_code: " << r.status_code << std::endl;
    switch (r.status_code) {
        case 204:
            abort();
        default:
            throw std::runtime_error("could not block user");
    }
}

void Onyx::SetOk() { has_access_ = true; }

inline bool Onyx::has_access() const noexcept { return has_access_; }
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
}  // namespace impl

static std::random_device rd;   // obtain a random number from hardware
static std::mt19937 gen(rd());  // seed the generator

inline void InitOnyx(const char* onyx_server_addr) {
    if (!impl::__onyxes.empty()) throw std::runtime_error("Onyx already initialized.");

    // Validate server OK
    cpr::Response r = cpr::Get(cpr::Url{std::string(onyx_server_addr) + "/api/ping"});
    if (r.status_code != 200) throw std::runtime_error("Onyx server unavailable.");
    impl::__onyx_server_addr = onyx_server_addr;

    // init smbios to get system info once
    InitSMBIOS();

    static std::uniform_int_distribution<> distr(1, 14);  // define the range
    int onyxes{distr(gen)};
    for (int i = 0; i < onyxes; i++) impl::__onyxes.push_back(new impl::Onyx);
    std::cout << impl::__onyxes.size() << " onyxes created" << std::endl;
}

inline bool Auth(const char* login, const char* password) {
    if (impl::__onyxes.empty())
        throw std::runtime_error("Onyx not initialized. Call onyx::InitOnyx() first.");

    static std::uniform_int_distribution<> distr(
        0,
        impl::__onyxes.size() - 1);  // define the range
    auto rand_ind = distr(gen);
    impl::Onyx* _onyx = impl::__onyxes.at(rand_ind);
    std::cout << "Choosing random onyx [" << rand_ind << "] "
              << "at address " << &_onyx << std::endl;
    _onyx->Auth(login, password);
    return true;
}

}  // namespace onyx
