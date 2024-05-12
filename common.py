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

IDX_BYTES = 1
PAYLOAD_LEN_BYTES = 2
HEADER_LEN = IDX_BYTES + PAYLOAD_LEN_BYTES

MAX_PACKET_SIZE = 30


def to_radio_packets(buf: bytes):

    packet_list = []
    #packet_list.append([TRANSMISSION_START])
    bytes_read = 0
    ctrl = 0

    # Fragment buf into chunks
    while bytes_read < len(buf):
        chunk = []
        num_bytes = min(len(buf) - bytes_read, MAX_PACKET_SIZE)
        
        chunk.append(ctrl.to_bytes(length=IDX_BYTES) + buf[bytes_read:bytes_read + num_bytes]) # take window 
        packet_list.append(chunk)
        bytes_read += num_bytes

    packet_list.append([b'\x01\xBA\xBE'])

    return packet_list


def from_radio_packets(buf):

    # create buffer for defragmented packet, ignore control
    #parsed_bytes = [None] * (len(buf) - 1)
    parsed_bytes = bytearray()
    for i in range(0, len(buf)):
        
        # first two bytes indicate packet index
        #idx = int.from_bytes(buf[i][0:IDX_BYTES])
        ctrl = buf[i][0]
        #if idx < 0 or idx > len(buf) - 1:
         #   pr_warn(f"from_radio_packets: idx out of range, expected 0 <= idx <= 255, got {idx}")
          #  return bytes()

        # third and fourth bytes indicate number of valid bytes in payload
        #parsed_bytes[idx] = buf[i][IDX_BYTES:]
        if ctrl == 1:
            break
        parsed_bytes.append(buf[i][IDX_BYTES:])
        
    #flattened = bytes([x for xs in parsed_bytes for x in xs])

    #return flattened
    return bytes(parsed_bytes)


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