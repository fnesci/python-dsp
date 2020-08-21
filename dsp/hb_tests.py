import unittest
import random
import hb_filters
import hb_downsampler
import hb_upsampler
import fir_filter


class TestUpsampler(unittest.TestCase):

    def test_filtering(self):
        input_len = 1000
        x = [10. * random.random() for x in range(input_len)]
        x_padded = [y for z in zip(x, [0.0] * len(x)) for y in z]
        up_sampler = hb_upsampler.HbUpsampler(hb_filters.default_hb)
        full_filter = fir_filter.FirFilter(hb_filters.default_hb)
        full_y = []
        full_filter.block_next(x_padded, full_y)
        full_y = [y if abs(y) > 1e-10 else 0.0 for y in full_y]
        print(full_y)
        hb_y = []
        up_sampler.block_next(x, hb_y)
        print(hb_y)
        self.assertEqual(len(full_y), len(hb_y))
        errors = [abs(a - b) for a, b in zip(full_y, hb_y)]
        max_error = max(errors)
        self.assertLessEqual(max_error, 1e-12)
        pass


class TestDownsampler(unittest.TestCase):

    def test_filtering(self):
        input_len = 1000
        x = [10. * random.random() for x in range(input_len)]
        down_sampler = hb_downsampler.HbDownsampler(hb_filters.default_hb)
        full_filter = fir_filter.FirFilter(hb_filters.default_hb)
        full_y = []
        full_filter.block_next(x, full_y)
        trimmed_y = full_y[0::2]
        print(trimmed_y)
        hb_y = []
        down_sampler.block_next(x, hb_y)
        print(hb_y)
        self.assertEqual(len(trimmed_y), len(hb_y))
        errors = [abs(a - b) for a, b in zip(trimmed_y, hb_y)]
        max_error = max(errors)
        self.assertLessEqual(max_error, 1e-12)
        pass
