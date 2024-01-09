"""
Module with time converter functions.
"""

import lily_unit_test


TIME_UNITS = {'seconds': 1, 'minutes': 60, 'hours': 3600, 'days': 86400}


def create_duration_time_string(seconds):
    d, h = divmod(seconds, 86400)
    m, s = divmod(h, 60)
    h, m = divmod(m, 60)
    output = ''
    if d > 0:
        output = '%d days, ' % d
    output += '%02d:%02d:%02d' % (h, m, s)
    return output


def convert_seconds_to_time_with_unit(seconds):
    factor = 1
    for factor in sorted(TIME_UNITS.values(), reverse=True):
        if seconds % factor == 0:
            break
    unit = list(TIME_UNITS.keys())[list(TIME_UNITS.values()).index(factor)]
    return int(seconds / factor), unit


class TestTimeConverter(lily_unit_test.TestSuite):

    def test_create_duration_time_string(self):
        test_values = [
            (10, '00:00:10'),
            (200, '00:03:20'),
            (4000, '01:06:40'),
            (200000, '2 days, 07:33:20'),
        ]
        for test_value in test_values:
            self.fail_if(create_duration_time_string(test_value[0]) != test_value[1],
                         'Time string is incorrect')

    def test_convert_seconds_to_time_with_unit(self):
        test_values = [
            (10, (10, 'seconds')),
            (7200, (2, 'hours')),
            (180, (3, 'minutes')),
            (345600, (4, 'days')),
        ]
        for test_value in test_values:
            self.fail_if(convert_seconds_to_time_with_unit(test_value[0]) != test_value[1],
                         'Time string is incorrect')


if __name__ == '__main__':

    TestTimeConverter().run()
