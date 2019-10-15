from constants import _pi, _2pi
from helpers import *
import collections
import math

# This class implements a numerically controlled oscillator
class NcoInt:
    class TrigTable:
        def __init__(self, table_bits):
            self.table_bits = table_bits

    def __init__(self, w, inital_phase = 0, phase_bits = 32, table_bits = 8):
        self.max_phase = 1 << phase_bits
        self.phase_scale = _2pi / float(self.max_phase)
        # These will get set after calling the set functions
        self.w = None
        self.integer_phase = None
        self.delta_phase = None
        self.set_freq(w)
        self.set_phase(inital_phase)

    def __normalize_phase(self):
        """
        Takes the current integer_phase and converts it to the
        range [0, max_phase) using mode max_phase
        """
        if self.integer_phase >= self.max_phase:
            self.integer_phase -= self.max_phase

    def  set_phase(self, phase):
        """
        Set's the NCO's phase to the supplied phase
        :param phase: The phase to set the NCO to
        :return:
        """
        self.integer_phase = int((normalize_2pi(phase) * self.max_phase + _pi) / _2pi)
        self.__normalize_phase()

    def set_freq(self, w):
        """
        Sets the NCO's frequency to w
        :param w: The new frequency
        """
        self.w = normalize_pi(w)
        self.delta_phase = int((normalize_pi(w) * self.max_phase + _pi) / _2pi)

    def adjust_freq(self, d):
        self.w += d
        self.w = normalize_pi(self.w)
        self.delta_phase = int((normalize_pi(self.w) * self.max_phase + _pi) / _2pi)

    def __next_phase(self):
        self.integer_phase += self.delta_phase
        self.__normalize_phase()
        return self.integer_phase

    def next(self, num=1):
        """
        Updates the phase of the NCO
        :return:
        """
        if num == 1:
            iq = self.iq()
            self.__next_phase()
            return iq
        else:
            samples = collections.deque()
            while len(samples) < num:
                samples.append(self.iq())
                self.__next_phase()

            return samples

    def next_q(self, num=1):
        """
        Updates the phase of the NCO
        :return:
        """
        if num == 1:
            iq = self.iq()
            self.__next_phase()
            return iq.imag
        else:
            samples = collections.deque()
            while len(samples) < num:
                samples.append(self.iq().imag)
                self.__next_phase()

            return samples

    def next_i(self, num=1):
        """
        Updates the phase of the NCO
        :return:
        """
        if num == 1:
            iq = self.iq()
            self.__next_phase()
            return iq.real
        else:
            samples = collections.deque()
            while len(samples) < num:
                samples.append(self.iq().real)
                self.__next_phase()

            return samples

    def phase(self):
        """
        Returns the NCO's phase in the range [0, 2pi)
        :return:
        """
        return self.phase_scale * self.integer_phase

    def iq(self):
        """
        Retirns a tuple of (cos(phase), sin(phase))
        :return:
        """
        phase = self.phase()
        return complex(math.cos(phase), math.sin(phase))


class Nco:
    def __init__(self, w, inital_phase = 0, phase_bits = 32, table_bits = 8):
        # These will get set after calling the set functions
        self.w = None
        self.total_phase = None
        self.set_freq(w)
        self.set_phase(inital_phase)

    def  set_phase(self, phase):
        """
        Set's the NCO's phase to the supplied phase
        :param phase: The phase to set the NCO to
        :return:
        """
        self.total_phase = normalize_pi(phase)

    def set_freq(self, w):
        """
        Sets the NCO's frequency to w
        :param w: The new frequency
        """
        self.w = normalize_pi(w)

    def adjust_freq(self, d):
        self.w += d
        self.w = normalize_pi(self.w)

    def __next_phase(self):
        self.total_phase += self.w
        self.total_phase = normalize_pi(self.total_phase)
        return self.total_phase

    def next(self, num=1):
        """
        Updates the phase of the NCO
        :return:
        """
        if num == 1:
            iq = self.iq()
            self.__next_phase()
            return iq
        else:
            samples = collections.deque()
            while len(samples) < num:
                samples.append(self.iq())
                self.__next_phase()

            return samples

    def next_q(self, num=1):
        """
        Updates the phase of the NCO
        :return:
        """
        if num == 1:
            iq = self.iq()
            self.__next_phase()
            return iq.imag
        else:
            samples = collections.deque()
            while len(samples) < num:
                samples.append(self.iq().imag)
                self.__next_phase()

            return samples

    def next_i(self, num=1):
        """
        Updates the phase of the NCO
        :return:
        """
        if num == 1:
            iq = self.iq()
            self.__next_phase()
            return iq.real
        else:
            samples = collections.deque()
            while len(samples) < num:
                samples.append(self.iq().real)
                self.__next_phase()

            return samples

    def phase(self):
        """
        Returns the NCO's phase in the range [0, 2pi)
        :return:
        """
        return self.total_phase

    def iq(self):
        """
        Retirns a tuple of (cos(phase), sin(phase))
        :return:
        """

        return complex(math.cos(self.total_phase), math.sin(self.total_phase))

    def adjust_phase(self, phase_delta):
        self.total_phase += phase_delta
        self.total_phase = normalize_pi(self.total_phase)

