import asyncio

from . import tello_protocol


async def send_command(command):
    loop = asyncio.get_running_loop()
    # create callback to report finished status
    done_callback = loop.create_future()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: tello_protocol.TelloProtocol(command, done_callback),
        local_addr=client_address,
        remote_addr=tello_address)

    try:
        await asyncio.wait_for(done_callback, timeout=socket_timeout)
    except asyncio.TimeoutError:
        print('Network timeout, close the socket')
    finally:
        transport.close()
        # workaround for asynchronous socket close
        # https://stackoverflow.com/questions/35872750/how-to-close-python-asyncio-transport
        await asyncio.sleep(0)


async def send_commands(commands):
    for command in commands:
        await send_command(command)


# Initialize module
client_address = ('0.0.0.0', 8889)
tello_address = ('192.168.10.1', 8889)

socket_timeout = 2.0
