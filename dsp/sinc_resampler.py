import collections
import math
import numpy
from sinc import sinc
from table_function import TableFunction


def get_sinc_filter(freq, gain, N, window_function):
    assert N & 1 # Excepting an odd number of points
    W = N // 2 # Number of points on one side (aka wing)
    H = float(W)
    f = lambda x: 0.0 if math.fabs(x) >= W else window_function(x + H, N) * sinc(x, freq, gain)
    #f = lambda x: 0.0 if math.fabs(x) >= W else window_function(x + H, N) * gain * numpy.sinc(x * freq / math.pi)

    return f


class SincResampler:
    """
    Notes:  Implement multiple factory functions that do the following:
        1) Uses no half-band filters
        2) Uses a windowed sinc function for the filter
        3) Uses creates a
    """
    SinkResampleSettings = collections.namedtuple("SinkResampleSettings",
                                                  "ResampleRatio FilterLength WingLength OutputSampleStepSize SincFreq SincGain NumHBs")

    @staticmethod
    def get_settings(resample_ratio, filter_len, use_half_band_filters):
        if use_half_band_filters:
            # TODO: What corner cases should the code look for?
            #  such as don't use a HBF if the resample
            #  ratio is 0.5?
            num_halfbands = int(math.log2(resample_ratio))
            resample_ratio *= math.pow(2.0, -num_halfbands)
        else:
            num_halfbands = 0

        resample_ratio = float(resample_ratio)
        output_sample_step_size = 1.0 / resample_ratio
        wing_len = int(filter_len) // 2
        filter_len = 2 * wing_len + 1
        sinc_gain = min(1.0, 1.0 / resample_ratio)
        sinc_freq = 1.0 * math.pi * min(1.0, resample_ratio)
        return SincResampler.SinkResampleSettings(resample_ratio, filter_len, wing_len, output_sample_step_size, sinc_freq, sinc_gain, num_halfbands)

    @staticmethod
    def create_no_hb_no_tf():
        """
        Creates a sinc resampler that doesn't use any half-band filters and a windowed sinc
        :return:
        """
        return None

    @staticmethod
    def create_no_hb():
        """
        Creates a sinc resampler that doesn't use any half-band filters but uses a table
        function for looking up the windowed sinc
        :return:
        """
        return None

    def __init__(self, resample_ratio, filter_len, window, table_entries_per_zero_crossing):
        self.settings = SincResampler.get_settings(resample_ratio, filter_len, False)
        self.samples = collections.deque()
        self.next_resample_available = float(self.settings.FilterLength) - 1.0
        self.epsilon = 0.0
        self.right_len = self.settings.WingLength + 1
        self.left_len = self.settings.WingLength
        self.filter = get_sinc_filter(self.settings.SincFreq, self.settings.SincGain, self.settings.FilterLength, window)
        self.table = TableFunction(self.filter, -self.settings.WingLength, self.settings.WingLength,
                                   table_entries_per_zero_crossing * self.settings.WingLength)
        self.use_table_function = False
        self.use_table_function = True

    def add_samples(self, samples):
        self.samples.extend(samples)

    def resample(self):
        resamples = []
        while self.next_resample_available < len(self.samples):
            # Filter the samples
            # print("---")
            # print("NRA: {}, LI: {}, D: {}".format(self.next_resample_available, self.next_resample_available, self.epsilon))
            if not self.use_table_function:
                r = int(self.next_resample_available)
                sr = self.epsilon - self.settings.WingLength
                l = int(self.next_resample_available) - self.settings.FilterLength + 1
                sl = self.epsilon + self.settings.WingLength
                p = 0.0
                for i in range(self.settings.WingLength):
                    #print("q{} {:8.4f} {:8.4f}".format(l, sl, self.filter(sl)))
                    #print("p{} {:8.4f} {:8.4f}".format(r, sr, self.filter(sr)))
                    p += self.filter(sr) * self.samples[r] \
                         + self.filter(sl) * + self.samples[l]
                    r -= 1
                    sr += 1.0
                    l += 1
                    sl -= 1.0
                p += self.filter(self.epsilon) * self.samples[l]
            else:
                # p = 0.0
                # n = int(self.next_resample_available) - self.settings.FilterLength + 1
                # x = self.settings.FilterLength / 2 + self.epsilon
                # while n <= self.next_resample_available:
                #     #print("{} {:8.4f} {:8.4f}".format(n, x, self.filter(x)))
                #     p += self.table.evaluate(x) * self.samples[n]
                #     n += 1
                #     x -= 1.0
                # break_here = 0.0
                # pass

                r = int(self.next_resample_available)
                sr = self.epsilon - self.settings.WingLength
                l = int(self.next_resample_available) - self.settings.FilterLength + 1
                sl = self.epsilon + self.settings.WingLength
                p = 0.0
                for i in range(self.settings.WingLength):
                    #print("q{} {:8.4f} {:8.4f}".format(l, sl, self.filter(sl)))
                    #print("p{} {:8.4f} {:8.4f}".format(r, sr, self.filter(sr)))
                    p += self.table.evaluate(sr) * self.samples[r] \
                         + self.table.evaluate(sl) * + self.samples[l]
                    r -= 1
                    sr += 1.0
                    l += 1
                    sl -= 1.0
                p += self.table.evaluate(self.epsilon) * self.samples[l]

            # Save the resampled point
            #print len(resamples), p
            resamples.append(p)

            # What's the next point
            self.epsilon += self.settings.OutputSampleStepSize
            while self.epsilon >= 1.0:
                self.epsilon -= 1.0
                self.next_resample_available += 1.0

        # Get rid of points that won't be used in future updates
        points_to_dump = int(math.floor(self.next_resample_available) - self.settings.FilterLength)
        #points_to_dump = 0
        if points_to_dump > 0:
            self.next_resample_available -= points_to_dump
            # no easy multi-pop
            while points_to_dump != 0:
                points_to_dump -= 1
                self.samples.popleft()

        return resamples
