import asyncio

import tello.tello_stats_protocol as tello_stats_protocol


async def main():
    print('Starting tello stats server')

    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: tello_stats_protocol.TelloStatsProtocol(),
        local_addr=server_address)

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()


# Initialize module
server_address = ('0.0.0.0', 8890)

if __name__ == '__main__':
    print('Server address:', server_address)
    asyncio.run(main())
