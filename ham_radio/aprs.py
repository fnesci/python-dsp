import collections
import math

_aprs_settings = collections.namedtuple('AprsSettings', 'sample_rate samples_per_symbol mark_freq space_freq')


_decoder_sample_rate = 44100


def get_settings(sample_rate):
    bell_202_mark_hz = 1200
    bell_202_space_hz = 2200
    bell_202_baud_rate = 1200

    # When the data is made analytic, the sample rate will be halved
    half_sample_rate = 0.5 * sample_rate
    samples_per_symbol = float(half_sample_rate) / float(bell_202_baud_rate)
    freq_offset = 0.5 * (bell_202_space_hz - bell_202_mark_hz)
    # space_freq = 2 * math.pi * freq_offset / half_sample_rate
    space_freq = 2 * freq_offset / half_sample_rate
    mark_freq = -space_freq

    return _aprs_settings(sample_rate, samples_per_symbol, mark_freq, space_freq)


def factory(sample_rate):
    pass


class Encoder:
    pass


class Decoder:
    def __init__(self, source_sample_rate):
        self.source_sample_rate = source_sample_rate
        self.decoder_sample_rate = _decoder_sample_rate
        self.resampler = None
        self.make_analytic = None
        self.pll = None
        self.moving_average_filter = None
        self.timing_recovery = None
        pass
