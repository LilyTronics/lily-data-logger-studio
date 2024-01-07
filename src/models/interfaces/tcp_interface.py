"""
TCP client interface.
"""

import socket
import threading

from src.models.interfaces.interface import Interface
from unit_test.test_suite import TestSuite


class TcpInterface(Interface):

    def __init__(self, server_ip_address, server_port, timeout, rx_buffer_size=1500):
        self._server_ip_address = server_ip_address
        self._server_port = server_port
        self._timeout = timeout
        self._rx_buffer_size = rx_buffer_size
        self._socket = None

    def send_command(self, command):
        response = b''
        try:
            self._socket = socket.create_connection((self._server_ip_address, self._server_port), self._timeout)
        except (Exception, ):
            self.raise_connection_exception(f'{self._server_ip_address}:{self._server_port}')

        self._socket.sendall(command)
        try:
            response = self._socket.recv(self._rx_buffer_size)
        except TimeoutError:
            self.raise_timeout_exception()

        return response

    def close(self):
        if self._socket is not None:
            self._socket.close()


class TestTcpInterface(TestSuite):

    _IP = 'localhost'
    _PORT = 21000
    _CLIENT_TIMEOUT = 0.5
    _SERVER_TIMEOUT = 0.1
    _RX_BUFFER_SIZE = 1500
    _TEST_DATA = b'test TCP interface'
    _TEST_TIMEOUT_DATA = b'do_timeout'

    _socket = None
    _stop_event = None
    _thread = None

    def _process_data(self):
        while not self._stop_event.is_set():
            try:
                connection, client_address = self._socket.accept()
            except TimeoutError:
                continue
            data = connection.recv(self._RX_BUFFER_SIZE)
            if data == self._TEST_TIMEOUT_DATA:
                continue
            connection.sendall(data)

    def _start_server(self):
        self._socket = socket.create_server((self._IP, self._PORT))
        self._socket.settimeout(self._SERVER_TIMEOUT)
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._process_data)
        self._thread.daemon = True
        self._thread.start()

    def setup(self):
        self._client = TcpInterface(self._IP, self._PORT, self._CLIENT_TIMEOUT)

    def test_no_server_running(self):
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

    def test_server_running(self):
        self._start_server()
        response = self._client.send_command(self._TEST_DATA)
        self.log.debug('Response: {}'.format(response))
        self.fail_if(response != self._TEST_DATA, 'Invalid response received, expected: {}'.format(self._TEST_DATA))

    def test_timeout(self):
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

    TestTcpInterface().run(True)
