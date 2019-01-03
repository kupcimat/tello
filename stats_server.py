import asyncio
import configparser


class TelloStatsProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        print(f'Received {data.decode()} from {addr}')


async def main(server_address):
    print('Starting tello stats server')

    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: TelloStatsProtocol(),
        local_addr=server_address)

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read_file(open('properties.cfg'))

    server_address = (config['stats-server']['ip'], config['stats-server']['port'])

    print('Server address:', server_address)

    asyncio.run(
        main(server_address))
