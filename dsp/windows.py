import math
from scipy.special import jv

def retangular(N):
    return lambda n: 1.0


def blackman_harris(N):
    if N == 1:
        return [1.0]

    w2 = 2.0 * math.pi / (N - 1)
    w4 = 4.0 * math.pi / (N - 1)
    w6 = 6.0 * math.pi / (N - 1)
    _N = N
    bh = lambda n: 0.35875 - 0.48829 * math.cos(w2 * n) \
                             + 0.14128 * math.cos(w4 * n) \
                             - 0.01168 * math.cos(w6 * n)

    return bh
    # w = []
    # for n in range(N):
    #     w.append(bh(n))
    #
    # return w