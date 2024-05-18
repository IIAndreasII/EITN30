from pyrf24 import RF24, RF24_PA_LOW, RF24_1MBPS, RF24_2MBPS

from math import ceil

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
    radio_send.setDataRate(RF24_2MBPS)  # Options are 1MBPS, 2MBPS, 250KBPS
    radio_recv.setDataRate(RF24_2MBPS)

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
HEADER_LEN = IDX_BYTES + PAYLOAD_LEN_BYTES

MAX_PACKET_SIZE = 30


def to_radio_packets(buf: bytes):

    packet_list = []
    #packet_list.append([TRANSMISSION_START])
    bytes_read = 0
    ctrl = 0

    max_fragments = ceil(len(buf) / MAX_PACKET_SIZE)

    # Fragment buf into chunks
    while bytes_read < len(buf):
        chunk = []
        num_bytes = min(len(buf) - bytes_read, MAX_PACKET_SIZE)
        head = 0
        if ctrl == max_fragments - 1:
            head = b'\xff\xff'
        else:
            head = ctrl.to_bytes(length=IDX_BYTES)
        
        chunk.append(head + buf[bytes_read:bytes_read + num_bytes]) # take window 
        packet_list.append(chunk)
        bytes_read += num_bytes
        ctrl += 1

    packet_list[-1]

    return packet_list


def from_radio_packets(buf):

    # create buffer for defragmented packet, ignore control
    #parsed_bytes = [None] * (len(buf) - 1)
    parsed_bytes = bytes()
    for i in range(0, len(buf)):
        parsed_bytes += buf[i][IDX_BYTES:]
        
    #flattened = bytes([x for xs in parsed_bytes for x in xs])

    #return flattened
    return parsed_bytes


def pr_info(s):
    print("[info]", s)

debug = False

def pr_dbg(s):
    if debug:
        print("[dbg]", s)

def pr_warn(s):
    print("[warn]", s)

def pr_err(s):
    print("[err]", s)