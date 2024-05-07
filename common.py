from pyrf24 import RF24, RF24_PA_LOW, RF24_1MBPS


# GPIO for spidev0.1
CSN_PIN_SEND = 0
CE_PIN_SEND = 17

# GPIO for spidev1.0
CSN_PIN_RECV = 10
CE_PIN_RECV = 27


def setup_radios():
# Initialize the RF24 object with the CE and CSN pin numbers
    radio_send = RF24(CE_PIN_SEND, CSN_PIN_SEND)
    radio_recv = RF24(CE_PIN_RECV, CSN_PIN_RECV)

    # Begin operation of the radio module
    if not radio_send.begin():
        raise RuntimeError("NRF24L01+ hardware is not responding")

    if not radio_recv.begin():
        raise RuntimeError("NRF24L01+ hardware is not responding")


    # Set the PA Level (Power Amplifier Level)
    radio_send.setPALevel(RF24_PA_LOW)  # Options are MIN, LOW, HIGH, MAXä
    radio_recv.setPALevel(RF24_PA_LOW)

    # Set the data rate
    radio_send.setDataRate(RF24_1MBPS)  # Options are 1MBPS, 2MBPS, 250KBPS
    radio_recv.setDataRate(RF24_1MBPS)

    # Optionally, you can enable dynamic payloads and auto-acknowledgment features
    radio_send.enableDynamicPayloads()
    radio_send.enableAckPayload()

    radio_recv.enableDynamicPayloads()
    radio_recv.enableAckPayload()
    return radio_send, radio_recv


TRANSMISSION_START = b'\xCA\xFE\xCA\xFE\xCA\xFE\xCA\xFE\xCA\xFE\xCA\xFE\xCA\xFE\xCA\xFE\xCA\xFE\xCA\xFE\xCA\xFE\xCA\xFE\xCA\xFE\xCA\xFE\xCA\xFE\xCA\xFE'
TRANSMISSION_END   = b'\xBA\xBE\xBA\xBE\xBA\xBE\xBA\xBE\xBA\xBE\xBA\xBE\xBA\xBE\xBA\xBE\xBA\xBE\xBA\xBE\xBA\xBE\xBA\xBE\xBA\xBE\xBA\xBE\xBA\xBE\xBA\xBE'

IDX_BYTES = 2
PAYLOAD_LEN_BYTES = 2

MAX_PACKET_SIZE = 28


def to_radio_packets(buf: bytes):

    packet_list = []

    packet_list.append([TRANSMISSION_START])

    bytes_read = 0
    i = 0

    # Fragment buf into chunks
    while bytes_read < len(buf):
        chunk = []
        num_bytes = min(len(buf) - bytes_read, MAX_PACKET_SIZE)
        
        chunk.append(i.to_bytes(length=IDX_BYTES) + num_bytes.to_bytes(length=PAYLOAD_LEN_BYTES) + buf[bytes_read:bytes_read + num_bytes]) # take window 
        bytes_read += num_bytes
        i += 1
        packet_list.append(chunk)

    packet_list.append([TRANSMISSION_END])

    return packet_list


def from_radio_packets(buf):
    print(buf)
    #if buf[0] != [TRANSMISSION_START] or buf[-1] != [TRANSMISSION_END]:        
     #   raise Exception("Radio packet sanity check failed!")

    parsed_bytes = [None] * (len(buf) - 2) # ignore control
    for i in range(1, len(buf) - 1):
        #print(buf[i][0])
        idx = int.from_bytes(buf[i][0][0:2])
        #print(idx)
        pak_len = int.from_bytes(buf[i][0][2:4])
        #print(pak_len)
        parsed_bytes[idx] = buf[i][0][4:4+pak_len] # it is what it is
        #print(parsed_bytes[idx])

    #print(parsed_bytes)
    flattened = bytes([x for xs in parsed_bytes for x in xs])

    return flattened


# buf = bytes([1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1])

# packets = to_radio_packets(buf)

# #print(packets)

# flat = from_radio_packets(packets)
# print(flat)
# print(len(flat))
