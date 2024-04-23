# from pyrf24 import RF24, RF24_PA_LOW, RF24_1MBPS


# # GPIO for spidev0.1
# CSN_PIN_SEND = 0
# CE_PIN_SEND = 17

# # GPIO for spidev1.0
# CSN_PIN_RECV = 10
# CE_PIN_RECV = 27


# def setup_radios():
# # Initialize the RF24 object with the CE and CSN pin numbers
#     radio_send = RF24(CE_PIN_SEND, CSN_PIN_SEND)
#     radio_recv = RF24(CE_PIN_RECV, CSN_PIN_RECV)

#     # Begin operation of the radio module
#     if not radio_send.begin():
#         raise RuntimeError("NRF24L01+ hardware is not responding")

#     if not radio_recv.begin():
#         raise RuntimeError("NRF24L01+ hardware is not responding")


#     # Set the PA Level (Power Amplifier Level)
#     radio_send.setPALevel(RF24_PA_LOW)  # Options are MIN, LOW, HIGH, MAXä
#     radio_recv.setPALevel(RF24_PA_LOW)

#     # Set the data rate
#     radio_send.setDataRate(RF24_1MBPS)  # Options are 1MBPS, 2MBPS, 250KBPS
#     radio_recv.setDataRate(RF24_1MBPS)

#     # Optionally, you can enable dynamic payloads and auto-acknowledgment features
#     radio_send.enableDynamicPayloads()
#     radio_send.enableAckPayload()

#     radio_recv.enableDynamicPayloads()
#     radio_recv.enableAckPayload()

#     return radio_send, radio_recv


TRANSMISSION_START = b'\xCA\xFE'
TRANSMISSION_END   = b'\xBA\xBE'


MAX_PACKET_SIZE = 20


def to_radio_packets(buf: bytes):

    packet_list = []

    packet_list.append([TRANSMISSION_START])

    bytes_read = 0
    i = 0

    # Fragment buf into chunks
    while bytes_read < len(buf):
        chunk = []
        num_bytes = min(len(buf) - bytes_read, MAX_PACKET_SIZE)
        
        chunk.append(i.to_bytes() + buf[bytes_read:bytes_read + num_bytes]) # take window 
        bytes_read += num_bytes
        i += 1
        packet_list.append(chunk)

    packet_list.append([TRANSMISSION_END])

    return packet_list


def from_radio_packets(buf):

    return bytes()


buf = bytes([1,2,3,4,5,6,7,8,9,0])

packets = to_radio_packets(buf)

print(packets)