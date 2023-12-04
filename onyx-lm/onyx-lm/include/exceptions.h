#pragma once

#include <exception>

namespace onyx {
namespace exceptions {
class AlreadyLoggedIn : public std::exception {
   public:
    const char* what() const throw() { return "Logged in on other device"; }
};
class Blocked : public std::exception {
   public:
    const char* what() const throw() { return "Blocked"; }
};
class BadCredentials : public std::exception {
   public:
    const char* what() const throw() { return "Wrong username or password"; }
};
}  // namespace exceptions
}  // namespace onyx
