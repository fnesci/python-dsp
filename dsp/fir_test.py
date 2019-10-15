import fir_filter
import math
import _nco

import unittest

class Test(unittest.TestCase):
    pass
    def test_impulse_response(self):
        fir = fir_filter.FirFilter(Test.h)
        x = [0.0] * (fir.N() + 1)
        x[0] = 1.0
        y = []
        fir.block_next(x, y)
        print(x)
        print(y)
        self.assertTrue(True)

    def test_high_stop(self):
        nco = _nco.Nco(0.75 * math.pi)

        x = nco.next(100)
        fir = fir_filter.FirFilter(Test.h)
        x[0] = 1.0
        y = []
        fir.block_next(x, y)
        y = [abs(i) for i in y]
        print(x)
        print(y)
        self.assertTrue(True)

    def test_low_pass(self):
        nco = _nco.Nco(0.15 * math.pi)

        x = nco.next(100)
        fir = fir_filter.FirFilter(Test.h)
        x[0] = 1.0
        y = []
        fir.block_next(x, y)
        y = [abs(i) for i in y]
        print(x)
        print(y)
        self.assertTrue(True)

    h = [
        -0.000000000000000003,
        -0.006516192064016200,
        0.000000000000000006,
        0.014280311428581572,
        -0.000000000000000010,
        -0.027151498821544103,
        0.000000000000000013,
        0.049507622881582232,
        -0.000000000000000017,
        -0.097347574494857106,
        0.000000000000000019,
        0.316324531370552109,
        0.501805599399402946,
        0.316324531370552109,
        0.000000000000000019,
        -0.097347574494857106,
        -0.000000000000000017,
        0.049507622881582232,
        0.000000000000000013,
        -0.027151498821544103,
        -0.000000000000000010,
        0.014280311428581572,
        0.000000000000000006,
        -0.006516192064016197,
        -0.000000000000000003,
    ]