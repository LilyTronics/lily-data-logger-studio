"""
Temperature chamber using TCP interface.

Functions:
- get actual temperature
- set required temperature
- get required temperature
- get chamber state on / off
- set chamber state on / off

Temperature range :-30 to +90 degrees Celsius
Temperature change: 2 degrees / second
"""

import lily_unit_test
import socket
import threading
import time

from src.simulators.simulator_settings import SimulatorSettings


class TemperatureChamberTcp(object):

    _CMD_GET_STATE = b'STATE?'
    _CMD_SET_STATE = b'STATE='
    _CMD_GET_ACT_TEMP = b'ACT_TEMP?'
    _CMD_GET_SET_TEMP = b'SET_TEMP?'
    _CMD_SET_SET_TEMP = b'SET_TEMP='

    _RSP_UNKNOWN_COMMAND = b'UNKNOWN COMMAND'
    _RSP_OK = b'OK'
    _RSP_INVALID_VALUE = b'INVALID VALUE'

    _RX_BUFFER_SIZE = 1500
    _TERMINATOR = b'\n'

    _MIN_TEMPERATURE = -30.0
    _MAX_TEMPERATURE = 90.0
    _INITIAL_TEMPERATURE = 20.0
    _DEGREES_PER_SECOND = 2
    _TEMP_LOOP_STEP = 0.1
    _TEMP_LOOP_INTERVAL = _TEMP_LOOP_STEP / _DEGREES_PER_SECOND

    def __init__(self):
        self._tcp_thread = None
        self._tcp_stop_event = threading.Event()
        self._temperature_thread = None
        self._temperature_stop_event = threading.Event()
        self._lock = threading.RLock()
        self._socket = socket.create_server((SimulatorSettings.TemperatureChamberTcp.IP,
                                             SimulatorSettings.TemperatureChamberTcp.PORT))
        self._socket.settimeout(SimulatorSettings.TemperatureChamberTcp.RX_TIME_OUT)
        # Temperature chamber properties
        self._actual_temperature = self._INITIAL_TEMPERATURE
        self._set_temperature = self._INITIAL_TEMPERATURE

    def __del__(self):
        self.stop()
        self._socket.close()

    ###########
    # Private #
    ###########

    def _temperature_chamber_process(self):
        while not self._temperature_stop_event.is_set():
            self._lock.acquire()
            try:
                if self._actual_temperature < self._set_temperature:
                    self._actual_temperature += self._TEMP_LOOP_STEP
                elif self._actual_temperature > self._set_temperature:
                    self._actual_temperature -= self._TEMP_LOOP_STEP
            finally:
                self._lock.release()
            time.sleep(self._TEMP_LOOP_INTERVAL)

    def _start_temperature_thread(self):
        if self._temperature_thread is None or not self._temperature_thread.is_alive():
            self._temperature_stop_event.clear()
            self._temperature_thread = threading.Thread(target=self._temperature_chamber_process)
            self._temperature_thread.daemon = True
            self._temperature_thread.start()

    def _stop_temperature_thread(self):
        if self._is_temperature_thread_running():
            self._temperature_stop_event.set()
            self._temperature_thread.join()

    def _is_temperature_thread_running(self):
        return self._temperature_thread is not None and self._temperature_thread.is_alive()

    def _handle_messages(self):
        while not self._tcp_stop_event.is_set():
            try:
                connection = self._socket.accept()[0]
            except TimeoutError:
                continue
            data = connection.recv(self._RX_BUFFER_SIZE)
            response = self._RSP_UNKNOWN_COMMAND

            if data.endswith(self._TERMINATOR):
                data = data[:-1]

                if data == self._CMD_GET_STATE:
                    state = b'ON' if self._is_temperature_thread_running() else b'OFF'
                    response = b'STATE=' + state

                elif data.startswith(self._CMD_SET_STATE):
                    if data[len(self._CMD_SET_STATE):] == b'ON':
                        self._start_temperature_thread()
                        response = self._RSP_OK
                    elif data[len(self._CMD_SET_STATE):] == b'OFF':
                        self._stop_temperature_thread()
                        response = self._RSP_OK
                    else:
                        response = self._RSP_INVALID_VALUE

                elif data == self._CMD_GET_ACT_TEMP:
                    self._lock.acquire()
                    try:
                        response = b'ACT_TEMP=' + ('{:.1f}'.format(self._actual_temperature)).encode()
                    finally:
                        self._lock.release()

                elif data == self._CMD_GET_SET_TEMP:
                    self._lock.acquire()
                    try:
                        response = b'SET_TEMP=' + ('{:.1f}'.format(self._set_temperature)).encode()
                    finally:
                        self._lock.release()

                elif data.startswith(self._CMD_SET_SET_TEMP):
                    value = data[len(self._CMD_SET_SET_TEMP):]
                    self._lock.acquire()
                    try:
                        new_temp = float(value)
                        if new_temp < self._MIN_TEMPERATURE or new_temp > self._MAX_TEMPERATURE:
                            raise ValueError()
                        self._set_temperature = new_temp
                        response = self._RSP_OK
                    except ValueError:
                        response = self._RSP_INVALID_VALUE
                    finally:
                        self._lock.release()

            connection.sendall(response + self._TERMINATOR)

    ##########
    # Public #
    ##########

    def start(self):
        if self._tcp_thread is None or not self._tcp_thread.is_alive():
            self._tcp_stop_event.clear()
            self._tcp_thread = threading.Thread(target=self._handle_messages)
            self._tcp_thread.daemon = True
            self._tcp_thread.start()

    def stop(self):
        if self.is_running():
            self._stop_temperature_thread()
            self._tcp_stop_event.set()
            self._tcp_thread.join()

    def is_running(self):
        return self._tcp_thread is not None and self._tcp_thread.is_alive()


class TestTemperatureChamberTcp(lily_unit_test.TestSuite):

    _TERMINATOR = b'\n'
    _RX_BUFFER_SIZE = 1500
    _TEMP_TIMEOUT = 15

    def _log_running_threads(self):
        self.log.debug('Running threads: {}'.format(', '.join(map(lambda x: str(x), threading.enumerate()))))

    def _send_command(self, command):
        sock = socket.create_connection((SimulatorSettings.TemperatureChamberTcp.IP,
                                         SimulatorSettings.TemperatureChamberTcp.PORT),
                                        SimulatorSettings.TemperatureChamberTcp.RX_TIME_OUT)
        sock.sendall(command + self._TERMINATOR)
        return sock.recv(self._RX_BUFFER_SIZE)

    def setup(self):
        self._n_threads = len(threading.enumerate())
        self._temperature_chamber = TemperatureChamberTcp()

    def test_start_stop(self):
        self.log.debug('Start temperature chamber')
        self._temperature_chamber.start()
        self._log_running_threads()
        self.fail_if(len(threading.enumerate()) != self._n_threads + 1,
                     'The temperature chamber did not start properly')
        self.fail_if(not self._temperature_chamber.is_running(), 'The temperature chamber thread is not running')

        self.log.debug('Start temperature chamber while running')
        self._temperature_chamber.start()
        self.fail_if(len(threading.enumerate()) != self._n_threads + 1,
                     'The temperature chamber did not ignore start while running')
        self.fail_if(not self._temperature_chamber.is_running(),
                     'The temperature chamber thread is not running after start while running')

        self.log.debug('Stop temperature chamber')
        self._temperature_chamber.stop()
        self.fail_if(len(threading.enumerate()) != self._n_threads, 'The temperature chamber did not stop')
        self.fail_if(self._temperature_chamber.is_running(),
                     'The temperature chamber thread is still running after stop')

        self.log.debug('Stop temperature chamber while not running')
        self._temperature_chamber.stop()

        self.log.debug('Restart temperature chamber')
        self._temperature_chamber.start()
        self._log_running_threads()
        self.fail_if(len(threading.enumerate()) != self._n_threads + 1,
                     'The temperature chamber did not restart properly')
        self.fail_if(not self._temperature_chamber.is_running(), 'The temperature chamber thread is not running')

    def test_temperature_chamber_state(self):
        self.log.debug('Check initial state')
        response = self._send_command(b'STATE?')
        self.fail_if(response != b'STATE=OFF' + self._TERMINATOR, 'Invalid response received {}'.format(response))

        self.log.debug('Turn temperature chamber on')
        response = self._send_command(b'STATE=ON')
        self.fail_if(response != b'OK' + self._TERMINATOR, 'Invalid response received {}'.format(response))
        response = self._send_command(b'STATE?')
        self.fail_if(response != b'STATE=ON' + self._TERMINATOR, 'Invalid response received {}'.format(response))
        self._log_running_threads()
        self.fail_if(len(threading.enumerate()) != self._n_threads + 2,
                     'The temperature chamber process is not running')

        self.log.debug('Turn temperature chamber on while running')
        response = self._send_command(b'STATE=ON')
        self.fail_if(response != b'OK' + self._TERMINATOR, 'Invalid response received {}'.format(response))
        response = self._send_command(b'STATE?')
        self.fail_if(response != b'STATE=ON' + self._TERMINATOR, 'Invalid response received {}'.format(response))
        self._log_running_threads()
        self.fail_if(len(threading.enumerate()) != self._n_threads + 2,
                     'The temperature chamber did not ignore STATE=ON while running')

        self.log.debug('Turn temperature chamber off')
        response = self._send_command(b'STATE=OFF')
        self.fail_if(response != b'OK' + self._TERMINATOR, 'Invalid response received {}'.format(response))
        response = self._send_command(b'STATE?')
        self.fail_if(response != b'STATE=OFF' + self._TERMINATOR, 'Invalid response received {}'.format(response))
        self._log_running_threads()
        self.fail_if(len(threading.enumerate()) != self._n_threads + 1,
                     'The temperature chamber process did not stop')

        self.log.debug('Turn temperature chamber off while not running')
        response = self._send_command(b'STATE=OFF')
        self.fail_if(response != b'OK' + self._TERMINATOR, 'Invalid response received {}'.format(response))
        response = self._send_command(b'STATE?')
        self.fail_if(response != b'STATE=OFF' + self._TERMINATOR, 'Invalid response received {}'.format(response))

        self.log.debug('Turn temperature chamber on after turing off')
        response = self._send_command(b'STATE=ON')
        self.fail_if(response != b'OK' + self._TERMINATOR, 'Invalid response received {}'.format(response))
        response = self._send_command(b'STATE?')
        self.fail_if(response != b'STATE=ON' + self._TERMINATOR, 'Invalid response received {}'.format(response))
        self._log_running_threads()
        self.fail_if(len(threading.enumerate()) != self._n_threads + 2,
                     'The temperature chamber process is not running')

    def test_temperature_chamber_process(self):
        self.log.debug('Get actual temperature')
        response = self._send_command(b'ACT_TEMP?')
        self.fail_if(not (response.startswith(b'ACT_TEMP=') and response.endswith(self._TERMINATOR)),
                     'Invalid response received: {}'.format(response))
        act_temp = float(response[len(b'ACT_TEMP='):-1])
        self.log.debug('Actual temperature: {} degrees'.format(act_temp))

        self.log.debug('Increase temperature by 20 degrees')
        set_temp = act_temp + 20
        response = self._send_command(b'SET_TEMP=' + ('{:.1f}'.format(set_temp).encode()))
        self.fail_if(response != b'OK' + self._TERMINATOR, 'Invalid response received {}'.format(response))

        self.log.debug('Get set temperature')
        response = self._send_command(b'SET_TEMP?')
        self.fail_if(not (response.startswith(b'SET_TEMP=') and response.endswith(self._TERMINATOR)),
                     'Invalid response received: {}'.format(response))
        temp = float(response[len(b'SET_TEMP='):-1])
        self.fail_if(temp != set_temp, 'Set temperature value incorrect {}, expected {}'.format(temp, set_temp))

        self.log.debug('Wait for temperature to reach {:.1f} degrees, with timeout of {} seconds'.format(
                       set_temp, self._TEMP_TIMEOUT))
        t = self._TEMP_TIMEOUT
        while t > 0:
            time.sleep(1)
            response = self._send_command(b'ACT_TEMP?')
            temp = float(response[len(b'ACT_TEMP='):-1])
            if set_temp - 0.2 < temp < set_temp + 0.2:
                self.log.debug('Temperature is reached ({} degrees).'.format(temp))
                break
            t -= 1
        else:
            self.fail('Temperature was not reached within the timeout of {} seconds'.format(self._TEMP_TIMEOUT))

        self.log.debug('Decrease temperature by 20 degrees')
        set_temp = set_temp - 20
        response = self._send_command(b'SET_TEMP=' + ('{:.1f}'.format(set_temp).encode()))
        self.fail_if(response != b'OK' + self._TERMINATOR, 'Invalid response received {}'.format(response))

        self.log.debug('Get set temperature')
        response = self._send_command(b'SET_TEMP?')
        self.fail_if(not (response.startswith(b'SET_TEMP=') and response.endswith(self._TERMINATOR)),
                     'Invalid response received: {}'.format(response))
        temp = float(response[len(b'SET_TEMP='):-1])
        self.fail_if(temp != set_temp, 'Set temperature value incorrect {}, expected {}'.format(temp, set_temp))

        self.log.debug('Wait for temperature to reach {:.1f} degrees, with timeout of {} seconds'.format(
            set_temp, self._TEMP_TIMEOUT))
        t = self._TEMP_TIMEOUT
        while t > 0:
            time.sleep(1)
            response = self._send_command(b'ACT_TEMP?')
            temp = float(response[len(b'ACT_TEMP='):-1])
            if set_temp - 0.2 < temp < set_temp + 0.2:
                self.log.debug('Temperature is reached ({} degrees).'.format(temp))
                break
            t -= 1
        else:
            self.fail('Temperature was not reached within the timeout of {} seconds'.format(self._TEMP_TIMEOUT))

    def test_invalid_values(self):
        rsp_ok = b'OK\n'
        rsp_invalid_value = b'INVALID VALUE\n'
        self.log.debug('Test invalid state')
        response = self._send_command(b'STATE=INVALID')
        self.fail_if(response != rsp_invalid_value, 'Invalid response received {}'.format(response))

        set_temp = 91.0
        self.log.debug('Test 1 degree above maximum temperature ({} degrees)'.format(set_temp))
        response = self._send_command('SET_TEMP={:.1f}'.format(set_temp).encode())
        self.fail_if(response != rsp_invalid_value, 'Invalid response received {}'.format(response))

        set_temp = 90.0
        self.log.debug('Test with maximum temperature ({} degrees)'.format(set_temp))
        response = self._send_command('SET_TEMP={:.1f}'.format(set_temp).encode())
        self.fail_if(response != rsp_ok, 'Invalid response received {}'.format(response))

        set_temp = -31.0
        self.log.debug('Test 1 degree below minimum temperature ({} degrees)'.format(set_temp))
        response = self._send_command('SET_TEMP={:.1f}'.format(set_temp).encode())
        self.fail_if(response != rsp_invalid_value, 'Invalid response received {}'.format(response))

        set_temp = -30.0
        self.log.debug('Test with minimum temperature ({} degrees)'.format(set_temp))
        response = self._send_command('SET_TEMP={:.1f}'.format(set_temp).encode())
        self.fail_if(response != rsp_ok, 'Invalid response received {}'.format(response))

    def teardown(self):
        self._temperature_chamber.stop()
        self.fail_if(len(threading.enumerate()) != self._n_threads, 'The temperature chamber did not stop')
        self.fail_if(self._temperature_chamber.is_running(),
                     'The temperature chamber thread is still running after stop')


if __name__ == '__main__':
    TestTemperatureChamberTcp().run(True)
