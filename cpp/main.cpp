#include <ctime>
#include <iostream>
#include <iomanip>
#include <string>
#include "radio.h"
#include <chrono>
#include <thread>
#include "queue.h"
#include "tun.h"
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include "constants.h"

#define BASE

int setup_client_socket(int port);
int setup_server_socket(int port);

void tun_listen(std::shared_ptr<Tun> tun, std::shared_ptr<Queue<std::vector<uint8_t>>> transmitQueue);
void radio_receive(std::shared_ptr<Radio> radio, std::shared_ptr<Queue<std::vector<uint8_t>>> receiveQueue);
void radio_transmit(std::shared_ptr<Radio> radio, std::shared_ptr<Queue<std::vector<uint8_t>>> transmitQueue);
void tun_write(std::shared_ptr<Tun> tun, std::shared_ptr<Queue<std::vector<uint8_t>>> receiveQueue);

int main(int argc, char** argv)
{
    // UGLY
    //uint8_t address[4][6] = {"1Node", "2Node", "3Node", "4Node"};
    uint8_t addr1[6]{"1Node"};
    uint8_t addr2[6]{"2Node"};

#ifdef BASE
    auto rx = std::make_shared<Radio>(RadioMode::RX, CE_PIN_RECV, FIRST_CHANNEL, addr1);
    auto tx = std::make_shared<Radio>(RadioMode::TX, CE_PIN_SEND, SECOND_CHANNEL, addr2);
#else
    auto rx = std::make_shared<Radio>(RadioMode::RX, CE_PIN_RECV, SECOND_CHANNEL, addr2);
    auto tx = std::make_shared<Radio>(RadioMode::RX, CE_PIN_SEND, FIRST_CHANNEL, addr1);
#endif

    auto tun = std::make_shared<Tun>(DEV_NAME, 2);

    auto transmitQueue = std::make_shared<Queue<std::vector<uint8_t>>>();
    auto receiveQueue = std::make_shared<Queue<std::vector<uint8_t>>>();


    std::thread rxThread(radio_receive, rx, receiveQueue);
    std::thread tunWriteThread(tun_write, tun, receiveQueue);

    std::thread txThread(radio_transmit, tx, transmitQueue);
    std::thread tunReadThread(tun_listen, tun, transmitQueue);

    rxThread.join();
    txThread.join();
    tunWriteThread.join();
    tunReadThread.join();

    return 0;
}


void tun_listen(std::shared_ptr<Tun> tun, std::shared_ptr<Queue<std::vector<uint8_t>>> transmitQueue)
{
    uint8_t packet[MTU];
    size_t bytesRead{0};

    for(;;)
    {
        bytesRead = tun->Read(&packet, MTU);
        packet[bytesRead] = '\0';
        std::vector buf(packet, packet + bytesRead);

        if (buf.size() > 0)
            transmitQueue->push(buf);
    }
}

void tun_write(std::shared_ptr<Tun> tun, std::shared_ptr<Queue<std::vector<uint8_t>>> receiveQueue)
{
    for(;;)
    {
        bool done{false};
        std::vector<uint8_t> buf{};
        std::vector<uint8_t> packet{};

        while (!done && packet.size() < MTU)
        {
            receiveQueue->waitPop(buf);

            if (buf[0] == 1)
            {
                done = true;
                packet.insert(packet.end(), buf.begin() + 1, buf.end());
            }
        }

        if (done && packet.size() > 0)
            tun->Write(packet.data(), packet.size());
        
    }
}

void radio_transmit(std::shared_ptr<Radio> radio, std::shared_ptr<Queue<std::vector<uint8_t>>> transmitQueue)
{
#ifdef USE_UDP
    struct sockaddr_in sendto_address;
    int sockfd;

    memset(&sendto_address, 0, sizeof(sendto_address));
    sendto_address.sin_family = AF_INET;

    #ifdef BASE
        sockfd = setup_client_socket(4000);
        sendto_address.sin_port = htons(4000);
        sendto_address.sin_addr.s_addr = inet_addr(BASE_IP);
    #else
        sockfd = setup_client_socket(4001);
        sendto_address.sin_port = htons(4001);
        sendto_address.sin_addr.s_addr = inet_addr(CLIENT_IP);
    #endif
#endif

    for(;;) {
        std::vector<uint8_t> data;

        transmitQueue->waitPop(data);
#ifdef USE_UDP
        ssize_t bytes = sendto(sockfd, (const void*) data.data(), data.size(), MSG_CONFIRM, (const struct sockaddr*) &sendto_address, sizeof(sendto_address));
        std::cout << "Sending data: " << bytes << std::endl;
#else
        radio->Transmit(data);
#endif
    }
}

void radio_receive(std::shared_ptr<Radio> radio, std::shared_ptr<Queue<std::vector<uint8_t>>> receiveQueue)
{
#ifdef USE_UDP
    struct sockaddr_in recieve_addr;
    memset(&recieve_addr, 0, sizeof(recieve_addr));
    int sockfd;
    #ifdef BASE
        sockfd = setup_server_socket(4001);
    #else
        sockfd = setup_server_socket(4000);
    #endif
#endif

    for(;;) {
#ifdef USE_UDP
        uint8_t payload[MTU];
        ssize_t bytes;

        socklen_t len = sizeof(recieve_addr);
        bytes = recvfrom(sockfd, payload, MTU, 0, (struct sockaddr*)&recieve_addr, &len);
        std::cout << "Bytes recieved: " << bytes << std::endl;

        if(bytes > 0) {
            std::vector<uint8_t> data(payload, payload+bytes);
            receiveQueue->push(data);
        }
#else
        radio->Receive(receiveQueue);
#endif
    }
}

int setup_client_socket(int port)
{
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0); //IPv4, UDP, IP
    if (sockfd < 0) {
        std::cout << "client socket creation failed, port: " << port << std::endl;
    }

    return sockfd;
}

int setup_server_socket(int port)
{
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    int opt = 1;

    int sockfd = socket(AF_INET, SOCK_DGRAM, 0); //IPv4, UDP, IP
    if (sockfd < 0) {
        std::cout << "server socket failed, port: " << port << std::endl;
        return -1;
    }

    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        std::cout << "failed to setsockopt: " << port << std::endl;
        return -1;
    }

    memset(&address, 0, sizeof(address));

    address.sin_family = AF_INET;
    address.sin_port = htons(port);
    address.sin_addr.s_addr = INADDR_ANY;

    if (bind(sockfd, (struct sockaddr*)&address, addrlen) < 0) {
        std::cout << "failed to bind port: " << port << std::endl;
        return -1;
    }

    if (sockfd > 0) {
        std::cout << "server ready! port: " << port << std::endl;
    }

    return sockfd;
}
