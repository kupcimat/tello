import asyncio


class TelloProtocol(asyncio.DatagramProtocol):
    def __init__(self, command, done_callback):
        self.transport = None
        self.command = command
        self.done_callback = done_callback

    def connection_made(self, transport):
        self.transport = transport
        print('Send command:', self.command)
        self.transport.sendto(self.command.encode())

    def datagram_received(self, data, addr):
        print('Response:', data.decode())
        print('Close the socket')
        self.transport.close()

    def error_received(self, exc):
        print('Error:', exc)

    def connection_lost(self, exc):
        print('Connection closed')
        if not self.done_callback.cancelled():
            self.done_callback.set_result(True)
