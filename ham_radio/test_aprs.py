import ham_radio.aprs as aprs

import unittest

class Tests(unittest.TestCase):
    def test_settings(self):
        settings = aprs.get_settings(44100)
        print(settings)
        pass
