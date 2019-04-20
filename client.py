import sys

from tello.tello import Tello
from tello.tello_command import Command, GenericCommand

if __name__ == "__main__":
    tello = Tello()
    tello_commands = [Command()] + [GenericCommand(cmd) for cmd in sys.argv[1:]]

    for tello_command in tello_commands:
        tello.execute_command(tello_command)

    tello.join()
