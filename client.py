import asyncio
import sys

import tello.tello as tello
import tello.tello_command as command

if __name__ == '__main__':
    tello_commands = [command.Command()] + [command.GenericCommand(x) for x in sys.argv[1:]]
    asyncio.run(
        tello.send_commands(tello_commands))
