import queue
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

recv_q = queue.SimpleQueue()
send_q = queue.SimpleQueue()

running = True


def send():
    radio_send.open_tx_pipe(address[0])
    radio_send.listen = False

    while running:
        buf = send_q.get()
        start_timer = time.monotonic_ns()
        result = radio_send.write(buf)
        end_timer = time.monotonic_ns()
        if not result:
            print("Transmission failed or timed out")
        else:
            print(
                "Transmission successful! Time to Transmit:",
                f"{(end_timer - start_timer) / 1000} us"
            )
            val += 0.11
        time.sleep(1)
        count -= 1


def recieve():

    radio_recv.open_rx_pipe(0, b"2Node")    
    radio_recv.listen = True

    while running:
        has_payload, pipe_number = radio_recv.available_pipe()
        if has_payload:
            length = radio_recv.payload_size

            buf = radio_recv.read(length)
            recv_q.put(buf)
            print(f"Received {length} bytes on pipe {pipe_number}")

if __name__ == '__main__':
    p1 = Process(target=send, args=())
    p2 = Process(target=recieve, args=())
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()

   

