from _nco import Nco
import collections
import cmath
import fir_filter
import helpers

class Pll:
    default_loop_filter = [
    -0.000000000000000001,
    -0.008605955401424123,
    -0.021462748719213168,
    -0.024754777912840316,
    0.000000000000000007,
    0.061452102912016186,
    0.146309591373913916,
    0.221362761041361850,
    0.251398053412371147,
    0.221362761041361850,
    0.146309591373913916,
    0.061452102912016186,
    0.000000000000000007,
    -0.024754777912840316,
    -0.021462748719213168,
    -0.008605955401424123,
    -0.000000000000000001,
    ]

    @staticmethod
    def default_phase_detector(x, w):
        y = x * (w.real - 1j * w.imag)
        return cmath.phase(y)
        #return y.imag

    def __init__(self, phase_detector, phase_gain, freq_gain, loop_filter, w = 0):
        self.phase_detector = phase_detector
        self.phase_gain = phase_gain
        self.freq_gain = freq_gain
        self.loop_filter = fir_filter.FirFilter(loop_filter)
        self.w = w
        self.nco = Nco(w)

    def update(self, input):
        error_history = collections.deque()
        filtered_error_history = collections.deque()
        w_history = collections.deque()
        output = collections.deque()

        for x in input:
            w_history.append(self.nco.w)
            o = self.nco.next()
            output.append(o)
            error = self.phase_detector(x, o)
            error_history.append(error)
            error = self.loop_filter.next(error)
            filtered_error_history.append(error)
            phase_error = self.phase_gain * error
            freq_error = self.freq_gain * error
            self.nco.adjust_phase(phase_error)
            self.nco.adjust_freq(freq_error)

        return output, filtered_error_history, error_history, w_history

