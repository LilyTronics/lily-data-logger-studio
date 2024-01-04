"""
Send to a listening UDP port and process responses.
"""

import socket
import threading

from src.models.interfaces.interface import Interface
from unit_test.TestSuite import TestSuite


class UdpInterface(Interface):

    def __init__(self, server_ip_address, server_port, timeout):
        self._server_ip_address = server_ip_address
        self._server_port = server_port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.settimeout(timeout)

    def send_command(self, command):
        response = b''
        self._socket.sendto(command, (self._server_ip_address, self._server_port))
        try:
            response = self._socket.recvfrom(1024)
        except ConnectionResetError:
            self.raise_connection_exception(f'{self._server_ip_address}:{self._server_port}')
        except TimeoutError:
            self.raise_timeout_exception()

        return response

    def close(self):
        self._socket.close()


class TestUdpInterface(TestSuite):

    _IP = 'localhost'
    _PORT = 20000
    _TIMEOUT = 0.5
    _TEST_DATA = b'test UDP interface'
    _TEST_TIMEOUT_DATA = b'do_timeout'

    _socket = None
    _stop_event = None
    _thread = None

    def _process_data(self):
        while not self._stop_event.is_set():
            try:
                data, client_address = self._socket.recvfrom(1024)
                if data == self._TEST_TIMEOUT_DATA:
                    continue
                self._socket.sendto(data, client_address)
            except TimeoutError:
                pass

    def _start_server(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.settimeout(0.1)
        self._socket.bind((self._IP, self._PORT))
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._process_data)
        self._thread.daemon = True
        self._thread.start()

    def setup(self):
        self._client = UdpInterface(self._IP, self._PORT, self._TIMEOUT)

    def test_01_no_server_running(self):
        result = False
        try:
            self._client.send_command(self._TEST_DATA)
        except Exception as e:
            self.log.debug('Error message: {}'.format(e))
            if str(e).startswith('Could not connect to '):
                result = True
            else:
                self.log.error('Invalid error message, expect to start with: Could not connect to')
        return result

    def test_02_server_running(self):
        self._start_server()
        response = self._client.send_command(self._TEST_DATA)
        self.log.debug('Response: {}'.format(response[0]))
        assert response[0] == self._TEST_DATA, 'Invalid response received, expected: {}'.format(self._TEST_DATA)

    def test_03_timeout(self):
        result = False
        try:
            self._client.send_command(self._TEST_TIMEOUT_DATA)
        except Exception as e:
            self.log.debug('Error message: {}'.format(e))
            if str(e) == 'Error receiver timeout':
                result = True
            else:
                self.log.error('Invalid error message, expected: Error receiver timeout')
        return result

    def teardown(self):
        if None not in (self._socket, self._stop_event, self._thread):
            self._stop_event.set()
            self._thread.join()
            self._socket.close()
        self._client.close()


if __name__ == '__main__':

    TestUdpInterface().run()
