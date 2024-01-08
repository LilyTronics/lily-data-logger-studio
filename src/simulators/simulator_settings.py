"""
Container for simulator settings.
"""


class SimulatorSettings(object):

    class MultimeterUdp(object):
        IP = 'localhost'
        PORT = 17000
        RX_TIME_OUT = 0.2

    class TemperatureChamberTcp(object):
        IP = 'localhost'
        PORT = 17100
        RX_TIME_OUT = 0.2
