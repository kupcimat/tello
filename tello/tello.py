import asyncio
import threading

from tello.tello_protocol import TelloProtocol


class Tello:
    normal_priority = 100
    high_priority = 1

    def __init__(self):
        self.executor_loop = asyncio.new_event_loop()
        self.command_queue = asyncio.PriorityQueue(loop=self.executor_loop)
        self.command_count = 0
        # Start tello commands executor thread
        threading.Thread(target=start_executor,
                         args=(self.executor_loop, self.command_queue),
                         name="command-executor").start()

    def execute_command(self, tello_command, priority=normal_priority):
        print("Execute command:", tello_command.get_command())
        self.command_count += 1
        task = (priority, self.command_count, tello_command)
        asyncio.run_coroutine_threadsafe(
            self.command_queue.put(task), self.executor_loop).result()

    def join(self):
        asyncio.run_coroutine_threadsafe(
            self.command_queue.join(), self.executor_loop).result()
        self.close()

    def close(self):
        tasks = asyncio.all_tasks(self.executor_loop)
        asyncio.run_coroutine_threadsafe(
            cancel_executor_tasks(tasks), self.executor_loop).result()
        self.executor_loop.call_soon_threadsafe(stop_executor, self.executor_loop)


def start_executor(loop, command_queue):
    try:
        asyncio.set_event_loop(loop)
        loop.create_task(command_executor(command_queue))
        loop.run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


def stop_executor(loop):
    loop.stop()


async def cancel_executor_tasks(tasks):
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)


async def command_executor(command_queue):
    while True:
        _, _, tello_command = await command_queue.get()
        await send_command(tello_command)
        command_queue.task_done()


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
    except asyncio.CancelledError:
        print("Task cancelled, close the socket")
        raise
    finally:
        transport.close()
        # workaround for asynchronous socket close
        # https://stackoverflow.com/questions/35872750/how-to-close-python-asyncio-transport
        await asyncio.sleep(0)


# Initialize module
client_address = ("0.0.0.0", 8889)
tello_address = ("192.168.10.1", 8889)
socket_timeout = 15.0
