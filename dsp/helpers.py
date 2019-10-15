from constants import _2pi
from constants import _pi

def calc_omega_from_sample_rate(f, sample_rate):
    return _2pi  * f / sample_rate

def calc_omega_from_sample_period(f, sample_period):
    return _2pi * f * sample_period

def normalize_2pi(phase):
    """
    Converts phase to the range [0.0, pi)"
    :param phase:
    :return: The normalized phase
    """

    while phase < 0.0:
        phase += _2pi

    while phase >= _2pi:
        phase -= _2pi

    return phase

def normalize_pi(phase):
    """
    Converts phase to the range [-pi, pi)"
    :param phase:
    :return: The normalized phase
    """

    while phase < -_pi:
        phase += _2pi

    while phase >= _pi:
        phase -= _2pi

    return phase
