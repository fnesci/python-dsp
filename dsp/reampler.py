import collections
from constants import _2pi, _pi
import math
import numpy

# class FilterTable:
#     class TableEntry:
#         def __init__(self, x, y0, y1):
#             self.x = x
#             self.y = y0
#             self.delta = y1 - y0
#
#     def __init__(self, f, num_zero_crossings, entries_per_zero_crossing):
#         self.f = f
#         self.entries_per_zero_crossing = entries_per_zero_crossing
#         self.max_x = float(num_zero_crossings)
#         self.num_entries = int(num_zero_crossings * entries_per_zero_crossing)
#         self.step_size = self.max_x / (self.num_entries - 1.0)
#         self.entries = []
#         self.current_index = None
#         self.current_index_frac = None
#
#         for i in range(self.num_entries + 1):
#             x0 = i * self.max_x / self.num_entries
#             x1 = (i + 1) * self.max_x / self.num_entries
#             self.entries.append(SincResampler.FilterTable.TableEntry(x0, self.f(x0), self.f(x1)))
#
#     def set_inital_position(self, inital_crossing, offset):
#         # self.current_index = int(math.floor((inital_crossing + offset) * self.entries_per_zero_crossing))
#         # oe = offset * self.entries_per_zero_crossing
#         # mf = math.modf(offset * self.entries_per_zero_crossing)
#         # self.current_index_frac = mf[0]
#         l = (inital_crossing + offset) * self.entries_per_zero_crossing
#         mf = math.modf(l)
#         self.current_index = int(mf[1])
#         self.current_index_frac = mf[0]
#         pass
#
#     def eval(self):
#         e = self.entries[self.current_index]
#         return e.y + e.delta * self.current_index_frac
#
#     def next(self):
#         self.current_index += self.entries_per_zero_crossing
#
#     def prev(self):
#         self.current_index -= self.entries_per_zero_crossing


class SincResampler:
    @staticmethod
    def create_filter_function(N, wf, w_co):
        assert N & 1 == 1
        _N = float(N)
        shift = math.floor(0.5 * _N)
        w = wf(N)

        sinc_gain = 2.0 * min(1.0, w_co  / _2pi)
        sinc_freq = 2.0 * min(1.0, w_co / _2pi)

        h = lambda n : w(n + shift) * sinc_gain * numpy.sinc(sinc_freq * (n)) \
            if -shift <= n < shift else 0.0

        return h

    def __init__(self, resample_ratio, cutoff_freq, filter_length, window_generator, use_table_function = False):
        self.resample_ratio = float(resample_ratio)
        self.w_co = float(cutoff_freq)
        self.sinc_gain = min(1.0, self.resample_ratio)
        self.sinc_freq = min(1.0, self.resample_ratio)

        # The filter length should be odd
        self.filter_length = 2 * int(filter_length // 2) + 1
        # Create the window for the filter
        self.window_function  = window_generator
        self.filter = SincResampler.create_filter_function(self.filter_length, self.window_function, self.w_co)
        self.use_table_function = use_table_function

        self.right_len = self.filter_length // 2 + 1
        self.left_len = self.filter_length // 2
        self.samples = collections.deque()
        self.output_sample_step_size = 1.0 / self.resample_ratio
        self.next_resample_available = float(self.filter_length) - 1.0

        # generate the resample filter
        if self.use_table_function:
            # Generate
            pass
            assert False
        else:
            pass

    def get_filter(self):
        f = []
        offset = math.floor(0.5 * self.filter_length)
        for n in range(self.filter_length):
            f.append(self.filter(n - offset))

        return f

    def h(self, n):
        f = self.sinc_freq * n
        v = numpy.sinc(f)
        return self.sinc_gain * numpy.sinc(self.sinc_freq * n) * self.window(n + 0.5 * (self.filter_length - 1.0), self.filter_length)

    def s(self, n):
        f = self.sinc_freq * n
        v = numpy.sinc(f)
        return self.sinc_gain * numpy.sinc(self.sinc_freq * n)

    def w(self, n):
        return self.window(n + 0.5 * (self.filter_length - 1.0), self.filter_length)


    def add_samples(self, samples):
        '''
        This method adds sample to the list of input samples.  To generate resampled data
        call resample()
        :param samples: Sample to append to the list of input samples
        :return: None
        '''
        self.samples.extend(samples)

    def resample(self):
        resamples = []
        while self.next_resample_available < len(self.samples):
            # Filter the samples
            #print "---"
            delta, last_index = math.modf(self.next_resample_available)

            if not self.use_table_function:
                # Right wing
                # (left_len, -1]
                p = 0
                h_index = delta
                s_index = int(last_index) - self.right_len + 1
                for i in range(self.right_len):
                    #print("{} {} {:8.4}".format(s_index, h_index, self.filter(h_index)))
                    p += self.filter(h_index) * self.samples[s_index]
                    s_index += 1
                    h_index += 1.0

                # Left wing
                # [0, right_len)
                h_index = -delta - 1.0
                s_index = int(last_index) - self.right_len
                q = 0
                for i in range(self.left_len):
                    #print("{} {} {:8.4}".format(s_index, h_index, self.filter(h_index)))
                    q += self.filter(h_index) * self.samples[s_index]
                    s_index -= 1
                    h_index -= 1.0
            else:
                assert False
                p = 0.0

                zero_crossing = self.num_zero_crossings
                sample_index = int(last_index) - self.filter_length + 1
                self.table.set_inital_position(self.num_zero_crossings, delta)
                for i in range(self.left_len):
                    p += self.table.eval() * self.samples[sample_index]
                    self.table.prev()
                    sample_index += 1


                sample_index = int(last_index) - self.right_len + 1
                q = 0
                self.table.set_inital_position(self.num_zero_crossings, 1.0 - delta)
                for i in range(0, self.right_len):
                    q += self.table.eval() * self.samples[sample_index]
                    self.table.prev()
                    sample_index += 1

            p += q

            # Save the resampled point
            #print len(resamples), p
            resamples.append(p)

            # What's the next point
            self.next_resample_available += self.output_sample_step_size

        points_to_dump = int(math.floor(self.next_resample_available) - self.filter_length)
        #points_to_dump = 0
        if points_to_dump > 0:
            self.next_resample_available -= points_to_dump
            # no easy multi-pop
            while points_to_dump != 0:
                points_to_dump -= 1
                self.samples.popleft()

        return resamples


class CompositeResampler:
    def __init__(self, resample_ratio, cutoff_freq, filter_length, window_generator, use_table_function = False):
        self.resample_ratio = resample_ratio
        self.half_band_stages = int(math.log2(resample_ratio))
        self.sinc_resample_ratio = resample_ratio * math.pow(2.0, -self.half_band_stages)
