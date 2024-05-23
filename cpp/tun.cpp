#include "tun.h"
#include <fcntl.h>
#include <linux/if.h>
#include <linux/if_tun.h>
#include <memory.h>
#include <stdexcept>
#include <sys/ioctl.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <iostream>

#include "constants.h"

Tun::Tun(std::string name, int flags)// : myName(name)
{
    struct ifreq ifr;
    if ((devHandle = open("/dev/net/tun", O_RDWR)) < 0)
        throw std::runtime_error("Could not open tun device!");

    memset(&ifr, 0, sizeof(ifr));
    ifr.ifr_flags = IFF_TUN | IFF_NO_PI;

    if(name.data())
        strncpy(ifr.ifr_name, name.c_str(), name.size());

    int err;
    if((err = ioctl(devHandle, TUNSETIFF, (void *) &ifr)) < 0) {
        close(devHandle);
        throw std::runtime_error("ioctl returned " + std::to_string(err));
    }
    
    myName = ifr.ifr_name;

#if DEBUG
    std::cout << "Create TUN device:\n\tname: " << myName << std::endl;
#endif 
}

Tun::~Tun()
{
    if (devHandle != -1)
        close(devHandle);
}

size_t Tun::Read(void* buf, size_t size)
{
    ssize_t result = ::read(devHandle, buf, size);

    if (result < 0)
        std::cout << "Reading from tun failed: " << strerror(errno) << std::endl;
    
    return static_cast<size_t>(result);
}

size_t Tun::Write(void* buf, size_t size)
{
    ssize_t result = ::write(devHandle, buf, size);

    if (result < 0)
        std::cout << "Writing to tun failed: " << strerror(errno) << std::endl;

    return static_cast<size_t>(result);
}
