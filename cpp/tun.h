#ifndef __TUN_H__
#define __TUN_H__

#include <string>


class Tun
{
public:
    Tun() = delete;
    Tun(const std::string name, int flags);
    Tun(const Tun&) = delete;
    Tun(Tun&&) = delete;
    ~Tun();

    size_t Read(void *buf, size_t size);
    size_t Write(void *buf, size_t size);

private:
    std::string myName;
    int devHandle{0};
};


#endif