import fir_filter
import _nco

import math

class CostasLoop:
    def __init__(self, gain, initial_w, lpf_coefficients):
        self.gain = gain
        self.initial_w = initial_w
        self.nco = _nco.Nco(self.initial_w)
        self.lpf_coefficients = lpf_coefficients
        self.i_lpf = fir_filter.FirFilter(self.lpf_coefficients)
        self.q_lpf = fir_filter.FirFilter(self.lpf_coefficients)

    def next(self, samples):
        _i = []
        _q = []
        _si = []
        _sq = []
        _e = []
        _p = []
        _w = []

        for sample in samples:
            _p.append(self.nco.total_phase)
            _w.append(self.nco.w)
            phase = self.nco.next()
            i = sample * phase.real
            q = sample * phase.imag
            _i.append(i)
            _q.append(q)
            si = self.i_lpf.next(i)
            sq = self.q_lpf.next(q)
            _si.append(si)
            _sq.append(sq)
            e = math.atan2(sq, si)
            _e.append(e)
            #p = self.nco.total_phase + self.gain * e
            w = self.nco.w + self.gain * e
            #self.nco.set_phase(p)
            self.nco.set_freq(w)

        return _i, _q, _si, _sq, _e, _w