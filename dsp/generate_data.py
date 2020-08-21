import numpy as np
import wf

import sinc_resampler

def print_as_vector(name, data) :
    print "{"
    for e in data:
        print "{{{}, {}}},".format(e[0], e[1])
    print "};"


def generate_bh_sinc(max_x, num_points):
    nzc = 4
    dpzc = 3
    ratio = 1.0
    resamp = sinc_resampler.SincResampler(ratio, nzc, wf.blackman_harris, dpzc)

    sinc_freq = 1.0
    results = []
    window = wf.blackman_harris
    scale = 1.0 / (num_points - 1.0)
    for i in range(num_points):
        x = max_x * i * scale
        y = numpy.sinc(sinc_freq * x) * window(x + 0.5 * (num_points - 1.0), num_points)
        results.append((x, y))

    return results


if __name__ == '__main__':
    r = generate_bh_sinc(3.0, 31)
    print_as_vector('', r)
    print r