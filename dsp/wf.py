import math

RECTANGULAR = 0
TRIANGULAR = 1
HANN = 2
HAMMING = 3
BLACKMAN = 4
BLACKMAN_HARRIS = 5
KAISER = 6

def rectangular(n, N):
    return 1.0

def triangular(n, N):
    return max(0.0, 1.0 -  abs(2.0 * n - N + 1.0) / (N - 1.0))

def hann(n, N):
    return max(0.0, 0.5 * (1.0 - math.cos(2.0 * math.pi * n / (N - 1.0))))

def hamming(n, N):
    return max(0.0, 0.54 - 0.46 * math.cos(2.0 * math.pi * n / (N - 1.0)))

def blackman_harris(n, N):
    s = 2.0 * math.pi * n / (N - 1.0)
    return max(0.0, 0.35875 - 0.48829 * math.cos(s) + 0.14128 * math.cos(2.0 * s) - 0.01168 * math.cos(3.0 * s))


