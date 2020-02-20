import unittest
import random
import hb_filters
import hb_upsampler

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
        input_len = 5
        x = [random.random() for x in range(input_len)]
        x_padded = [y for z in zip(x, [0.0] * len(x)) for y in z]
        print(x_padded)
        pass
