import asyncio
import time


class EchoServerProtocol(asyncio.DatagramProtocol):
    def __init__(self, response, sleep):
        self.response = response
        self.sleep = sleep
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        print(f"Received {data.decode()} from {addr}")
        time.sleep(self.sleep)
        print(f"Send {self.response} to {addr}")
        self.transport.sendto(self.response.encode(), addr)


async def main():
    print("Starting UDP server")

    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    # One protocol instance will be created to serve all
    # client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol("ok", 3),
        local_addr=("0.0.0.0", 9999))

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()


asyncio.run(main())
