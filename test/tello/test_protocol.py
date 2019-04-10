from unittest.mock import Mock

from tello.tello_protocol import TelloProtocol


def test_connection_made():
    tello_protocol = TelloProtocol('test command', Mock())
    tello_protocol.connection_made(Mock())

    tello_protocol.transport.sendto.assert_called_once_with(b'test command')


def test_datagram_received():
    tello_protocol = TelloProtocol('test command', Mock())
    tello_protocol.connection_made(Mock())
    tello_protocol.datagram_received(b'test response', ('localhost', 9999))

    tello_protocol.transport.close.assert_called_once()


def test_error_received():
    tello_protocol = TelloProtocol('test command', Mock())
    tello_protocol.error_received(Exception('test error'))


def test_connection_lost():
    done_callback = Mock()
    done_callback.cancelled.return_value = False

    tello_protocol = TelloProtocol('test command', done_callback)
    tello_protocol.connection_lost(None)

    tello_protocol.done_callback.set_result.assert_called_once_with(True)


def test_connection_lost_timeout():
    done_callback = Mock()
    done_callback.cancelled.return_value = True

    tello_protocol = TelloProtocol('test command', done_callback)
    tello_protocol.connection_lost(None)

    tello_protocol.done_callback.set_result.assert_not_called()
