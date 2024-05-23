#ifndef __RADIO_H__
#define __RADIO_H__

#include <RF24/RF24.h>
#include <string>
#include <vector>
#include "queue.h"
#include <memory>

enum class RadioMode
{
    RX,
    TX
};

class Radio
{
public:
    Radio() = delete;
    Radio(const RadioMode mode, int ce, int channel, uint8_t addr[6]);

    Radio(Radio&& r) = delete;
    Radio(Radio& r) = delete;
    ~Radio() = default;

    void Transmit(const std::vector<uint8_t>& data);
    void Receive(std::shared_ptr<Queue<std::vector<uint8_t>>> recvQueue);

    void SetListen(const bool val);

private:
    RF24 myRadio;
};


#endif