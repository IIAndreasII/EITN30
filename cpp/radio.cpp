#include "radio.h"

#include <iostream>

#include "constants.h"

Radio::Radio(const RadioMode mode, int ce, int channel, uint8_t addr[6]) :
    myRadio()
{
    if (!myRadio.begin(ce, (ce == CE_PIN_RECV) * CSN_PIN_RECV))
    {
        throw std::runtime_error("Radio hardware failure!");
    }

    myRadio.enableDynamicPayloads();
    myRadio.setPALevel(RF24_PA_LOW);
    myRadio.setDataRate(RF24_2MBPS);
    myRadio.setCRCLength(RF24_CRC_8);
    myRadio.setRetries(0, 5);
    myRadio.setAutoAck(true);

    myRadio.setChannel(channel);

    switch(mode)
    {
        case RadioMode::RX:
            myRadio.openReadingPipe(1, addr);
            break;
        case RadioMode::TX:
            myRadio.openWritingPipe(addr);
            break;
        default:
            throw std::runtime_error("This should never happen");
    }

#if DEBUG
    std::cout << "Start radio:\n\tchannel: " << channel << "\n\taddr: " << addr << std::endl;
#endif

}

void Radio::Transmit(const std::vector<uint8_t>& data)
{
    size_t bytes_left{data.size()};
    size_t offset{0};

    while(bytes_left > 0)
    {
        uint8_t radioPacket[RADIO_PACKET_SIZE];
        memcpy(radioPacket + 1, data.data() + offset, std::min(bytes_left, size_t(RADIO_PACKET_SIZE - 1)));
        if (bytes_left < RADIO_PACKET_SIZE)
            radioPacket[0] = 0xff;
        else
            radioPacket[0] = 0x00;

        bool res = myRadio.writeFast(radioPacket, std::min(bytes_left + 1, size_t(32)));
        if (!res) {
            myRadio.txStandBy();
            res = myRadio.writeFast(radioPacket, std::min(bytes_left + 1, size_t(32)));
        }
        offset += std::min(bytes_left, size_t(31));
        bytes_left -= std::min(bytes_left, size_t(31));
    }
}

void Radio::Receive(std::shared_ptr<Queue<std::vector<uint8_t>>> recvQueue)
{
    uint8_t payload[32];
    uint8_t pipe;
    if (myRadio.available(&pipe)) {
        uint8_t bytes = myRadio.getDynamicPayloadSize();

        myRadio.read(&payload, bytes);

        // if (m_verbose) {
        //     std::cout << "Received " << std::dec << std::setw(0) << std::setfill(' ') << 32;
        //     std::cout << " bytes on pipe " << (unsigned int)pipe;
        //     std::cout << ": ";
        //     std::cout << std::setfill('0') << std::setw(2) << std::uppercase << std::hex;
        //     for (int i = 0; i < bytes; i++) {
        //         std::cout << int(payload[i]);
        //     }
        //     std::cout << std::endl;
        // }

        std::vector<uint8_t> data(payload, payload + 32);
        recvQueue->push(data);
    }
}


void Radio::SetListen(const bool val)
{
    if (val)
        myRadio.startListening();
    else
        myRadio.stopListening();
}