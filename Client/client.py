import sys
import struct
import time
sys.path.append('../')

import common

radio_send, radio_recv = common.setup_radios()

radio_send.setChannel(77)
radio_recv.setChannel(76)

address = [b"1Node"]


def recieve():
    timeout = 10
    radio_recv.open_rx_pipe(0, address[0])
    radio_recv.payload_size = struct.calcsize("<f")
    payload = [0.0]
    
    radio_recv.listen = True

    start = time.monotonic()
    while (time.monotonic() - start) < timeout:
        has_payload, pipe_number = radio_recv.available_pipe()
        if has_payload:
            length = radio_recv.payload_size  # grab the payload length
            # fetch 1 payload from RX FIFO
            received = radio_recv.read(length)  # also clears radio.irq_dr status flag
            # expecting a little endian float, thus the format string "<f"
            # received[:4] truncates padded 0s in case dynamic payloads are disabled
            payload[0] = struct.unpack("<f", received[:4])[0]
            # print details about the received packet
            print(f"Received {length} bytes on pipe {pipe_number}: {payload[0]}")
            start = time.monotonic()  # reset the timeout timer

recieve()
   

