import sys
import struct
import time
from multiprocessing import Process
sys.path.append('../')

import common

radio_send, radio_recv = common.setup_radios()

radio_send.setChannel(76)
radio_recv.setChannel(77)

address = [b"1Node"]

def send():
    radio_send.open_tx_pipe(address[0])
    radio_send.listen = False

    radio_send.payload_size = struct.calcsize('<f')
    val = 0.0

    count = 10
    while count:
        buf = struct.pack('<f', val)
        start_timer = time.monotonic_ns()
        result = radio_send.write(buf)
        end_timer = time.monotonic_ns()
        if not result:
            print("Transmission failed or timed out")
        else:
            print(
                "Transmission successful! Time to Transmit:",
                f"{(end_timer - start_timer) / 1000} us. Sent: {val}",
            )
            val += 0.11
        time.sleep(1)
        count -= 1


def recieve():
    timeout = 10
    radio_recv.open_rx_pipe(0, b"2Node")
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

if __name__ == '__main__':
    p1 = Process(target=send, args=())
    p2 = Process(target=recieve, args=())
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()

   

