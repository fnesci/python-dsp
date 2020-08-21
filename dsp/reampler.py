import collections
import math
import numpy

class FilterTable:
    class TableEntry:
        def __init__(self, x, y0, y1):
            self.x = x
            self.y = y0
            self.delta = y1 - y0

    def __init__(self, f, num_zero_crossings, entries_per_zero_crossing):
        self.f = f
        self.entries_per_zero_crossing = entries_per_zero_crossing
        self.max_x = float(num_zero_crossings)
        self.num_entries = int(num_zero_crossings * entries_per_zero_crossing)
        self.step_size = self.max_x / (self.num_entries - 1.0)
        self.entries = []
        self.current_index = None
        self.current_index_frac = None

        for i in range(self.num_entries + 1):
            x0 = i * self.max_x / self.num_entries
            x1 = (i + 1) * self.max_x / self.num_entries
            self.entries.append(SincResampler.FilterTable.TableEntry(x0, self.f(x0), self.f(x1)))

    def set_inital_position(self, inital_crossing, offset):
        # self.current_index = int(math.floor((inital_crossing + offset) * self.entries_per_zero_crossing))
        # oe = offset * self.entries_per_zero_crossing
        # mf = math.modf(offset * self.entries_per_zero_crossing)
        # self.current_index_frac = mf[0]
        l = (inital_crossing + offset) * self.entries_per_zero_crossing
        mf = math.modf(l)
        self.current_index = int(mf[1])
        self.current_index_frac = mf[0]
        pass

    def eval(self):
        e = self.entries[self.current_index]
        return e.y + e.delta * self.current_index_frac

    def next(self):
        self.current_index += self.entries_per_zero_crossing

    def prev(self):
        self.current_index -= self.entries_per_zero_crossing


class Resampler:
    @staticmethod
    def create_filter_function(N, w, w_co):
        assert N & 1 == 1
        _N = float(N)
        p = float(w_co) / (2.0 * math.pi)
        h = lambda n: w(n) * numpy.sinc(p * (n - _N + 1.0))
        pass

    def __init__(self, resample_ratio, cutoff_freq, filter_length, window_generator, use_table_function = False):
        self.resample_ratio = float(resample_ratio)
        self.w_co = float(cutoff_freq)

        # The filter length should be odd
        self.filter_length = 2 * int(filter_length / 2) + 1
        # Create the window for the filter
        self.window_function  = window_generator(self.filter_length)
        self.filter = Resampler.create_filter_function(self.filter_length, self.window_function, )
        self.use_table_function = use_table_function

        self.right_len = self.filter_length / 2 + 1
        self.left_len = self.filter_length / 2
        self.samples = collections.deque()
        self.output_sample_step_size = 1.0 / self.resample_ratio
        self.next_resample_available = float(self.filter_length) - 1.0

        # generate the resample filter
        self.filter = None
        if self.use_table_function:
            # Generate
            pass
        else:
            
        self.filter =
        self.sinc_gain = min(1.0, self.resample_ratio)
        self.sinc_freq = min(1.0, self.resample_ratio)
        self.table = SincResampler.FilterTable(self.h, num_zero_crossings, table_entries_per_zero_crossing)
        self.use_table_function = False
        self.use_table_function = True

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
                p = 0
                sample_index = int(last_index) - self.right_len
                for i in range(self.left_len):
                    #print "b{} {} {:8.4} {:8.4}".format(sample_index, i + delta, self.s(i + delta), self.w(i + delta))
                    p += self.h(i + delta) * self.samples[sample_index]
                    sample_index -= 1

                sample_index = int(last_index) - self.right_len + 1
                q = 0
                for i in range(0, self.right_len):
                    #print "{} {} {:8.4} {:8.4}".format(sample_index, i - delta + 1.0, self.s(i - delta + 1.0), self.w(i - delta + 1.0))
                    q += self.h(i - delta + 1.0) * self.samples[sample_index]
                    sample_index += 1
            else:
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