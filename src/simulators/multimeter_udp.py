"""
Multimeter using UDP interface.
"""

import lily_unit_test
import random
import socket
import threading

from src.simulators.simulator_settings import SimulatorSettings


class MultimeterUdp(object):

    CMD_VOLTAGE_DC = b'VDC?'
    CMD_CURRENT_DC = b'ADC?'

    _RX_BUFFER_SIZE = 1500
    _TERMINATOR = b'\n'

    _VDC_RANGE = (4.9, 5.1)
    _ADC_RANGE = (0.39, 0.41)

    def __init__(self):
        self._thread = None
        self._stop_event = threading.Event()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.settimeout(SimulatorSettings.MultimeterUdp.RX_TIME_OUT)
        self._socket.bind((SimulatorSettings.MultimeterUdp.IP, SimulatorSettings.MultimeterUdp.PORT))

    def __del__(self):
        self.stop()
        self._socket.close()

    ###########
    # Private #
    ###########

    def _do_measurement(self):
        while not self._stop_event.is_set():
            try:
                response = b'UNKNOWN COMMAND'
                data, client_address = self._socket.recvfrom(self._RX_BUFFER_SIZE)
                if self.CMD_VOLTAGE_DC + self._TERMINATOR == data:
                    response = 'VDC={:.3f}V'.format(random.uniform(*self._VDC_RANGE))
                elif self.CMD_CURRENT_DC + self._TERMINATOR == data:
                    response = 'ADC={:.3f}A'.format(random.uniform(*self._ADC_RANGE))
                self._socket.sendto(response.encode() + self._TERMINATOR, client_address)
            except TimeoutError:
                pass

    ##########
    # Public #
    ##########

    def start(self):
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._do_measurement)
            self._thread.daemon = True
            self._thread.start()

    def stop(self):
        if self.is_running():
            self._stop_event.set()
            self._thread.join()

    def is_running(self):
        return self._thread is not None and self._thread.is_alive()


class TestMultiMeterUdp(lily_unit_test.TestSuite):

    RX_TIME_OUT = 0.5
    RX_BUFFER_SIZE = 1500
    N_SAMPLES = 10
    TERMINATOR = b'\n'

    def log_running_threads(self):
        self.log.debug('Running threads: {}'.format(', '.join(map(lambda x: str(x), threading.enumerate()))))

    def send_command(self, command):
        self.socket.sendto(command + self.TERMINATOR, (SimulatorSettings.MultimeterUdp.IP, SimulatorSettings.MultimeterUdp.PORT))
        return self.socket.recvfrom(self.RX_BUFFER_SIZE)[0]

    def setup(self):
        self.multimeter = MultimeterUdp()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(self.RX_TIME_OUT)

    def test_start_stop(self):
        n_threads = len(threading.enumerate())
        self.log.debug('Start multimeter')
        self.multimeter.start()
        self.log_running_threads()
        self.fail_if(len(threading.enumerate()) != n_threads + 1, 'Multimeter did not start properly')
        self.fail_if(not self.multimeter.is_running(), 'The multimeter thread is not running')

        self.log.debug('Start multimeter while running')
        self.multimeter.start()
        self.fail_if(len(threading.enumerate()) != n_threads + 1, 'Multimeter did not ignore start while running')
        self.fail_if(not self.multimeter.is_running(), 'The multimeter thread is not running after start while running')

        self.log.debug('Stop multimeter')
        self.multimeter.stop()
        self.fail_if(len(threading.enumerate()) != n_threads, 'Multimeter did not stop')
        self.fail_if(self.multimeter.is_running(), 'The multimeter thread is still running after stop')

        self.log.debug('Stop multimeter while not running')
        self.multimeter.stop()

        self.log.debug('Restart multimeter')
        self.multimeter.start()
        self.log_running_threads()
        self.fail_if(len(threading.enumerate()) != n_threads + 1, 'Multimeter did not restart properly')
        self.fail_if(not self.multimeter.is_running(), 'The multimeter thread is not running')

    def test_voltage_dc(self):
        voltages = []
        self.log.debug('Get {} voltages'.format(self.N_SAMPLES))
        for i in range(self.N_SAMPLES):
            response = self.send_command(b'VDC?')
            self.fail_if(not response.startswith(b'VDC='), 'Response did not start with: VDC= ({})'.format(response))
            self.fail_if(not response.endswith(b'V\n'), 'Response did not end with: V\\n ({})'.format(response))
            voltages.append(float(response.strip()[4:-1]))
        self.log.debug('Voltages: {}'.format(voltages))
        self.fail_if(min(voltages) < 4.9, 'Voltage < 4.9 found: {}'.format(min(voltages)))
        self.fail_if(max(voltages) > 5.1, 'Voltage > 5.1 found: {}'.format(max(voltages)))

    def test_current_dc(self):
        currents = []
        self.log.debug('Get {} currents'.format(self.N_SAMPLES))
        for i in range(self.N_SAMPLES):
            response = self.send_command(b'ADC?')
            self.fail_if(not response.startswith(b'ADC='), 'Response did not start with: ADC= ({})'.format(response))
            self.fail_if(not response.endswith(b'A\n'), 'Response did not end with: A\\n ({})'.format(response))
            currents.append(float(response.strip()[4:-1]))
        self.log.debug('Currents: {}'.format(currents))
        self.fail_if(min(currents) < 0.39, 'Current < 0.39 found: {}'.format(min(currents)))
        self.fail_if(max(currents) > 0.41, 'Current > 0.41 found: {}'.format(max(currents)))

    def teardown(self):
        self.multimeter.stop()


if __name__ == '__main__':

    TestMultiMeterUdp().run(True)
