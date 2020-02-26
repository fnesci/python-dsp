import unittest
import random
import hb_filters
import hb_upsampler
import fir_filter

class TestUpsampler(unittest.TestCase):
    def test_filter_compression(self):
        up_sampler = hb_upsampler.HbUpsampler(hb_filters.default_hb)
        print(up_sampler.compressed_filter)
        hb_type_1 = [0]
        hb_type_1.extend(hb_filters.default_hb)
        hb_type_1.append([0])
        up_sampler = hb_upsampler.HbUpsampler(hb_type_1)
        print(up_sampler.compressed_filter)

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
