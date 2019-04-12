import asyncio

from tello.tello_protocol import TelloProtocol


async def send_command(tello_command):
    loop = asyncio.get_running_loop()
    # create callback to report finished status
    done_callback = loop.create_future()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: TelloProtocol(tello_command.get_command(), done_callback),
        local_addr=client_address,
        remote_addr=tello_address)

    try:
        await asyncio.wait_for(done_callback, timeout=socket_timeout)
    except asyncio.TimeoutError:
        print("Network timeout, close the socket")
    finally:
        transport.close()
        # workaround for asynchronous socket close
        # https://stackoverflow.com/questions/35872750/how-to-close-python-asyncio-transport
        await asyncio.sleep(0)


async def send_commands(tello_commands):
    for tello_command in tello_commands:
        await send_command(tello_command)


# Initialize module
client_address = ("0.0.0.0", 8889)
tello_address = ("192.168.10.1", 8889)
socket_timeout = 15.0
