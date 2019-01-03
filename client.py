import asyncio
import sys

import tello.tello as tello

if __name__ == '__main__':
    tello_commands = ['command'] + sys.argv[1:]
    asyncio.run(
        tello.send_commands(tello_commands))
