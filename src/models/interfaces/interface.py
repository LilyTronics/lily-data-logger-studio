"""
Base class for all the interfaces.
"""


class Interface(object):

    def raise_connection_exception(self, params):
        raise Exception(f'Could not connect to {params}')

    def raise_timeout_exception(self):
        raise Exception('Error receiver timeout')

    def send_command(self, *args):
        raise NotImplementedError('This method must be implemented in the derived class')

    def close(self):
        raise NotImplementedError('This method must be implemented in the derived class')
