import math

__epsilon = 1e-6
__a1 = -1.0 / math.factorial(3)
__a2 = 1.0 / math.factorial(5)
#__a3 = -1.0 / math.factorial(7)

def sinc(x, freq, gain):
    """
    Calculates and returns
        gain * sinc(freq * x)
    """
    x *= freq
    if math.fabs(x) < __epsilon:
        x2 = x * x
        return gain * (1.0 + x2 * (__a1 + x2 * (__a2)))
    else:
        return gain * math.sin(x) / x


if __name__ == '__main__':
    import numpy

    def crappy_sinc(x):
        return math.sin(x) / x

    x = 10.0
    scale = 0.95

    for i in range(1000):
        if i == 999:
            x = 0.0
        s = sinc(x, math.pi, 1.0)
        n = numpy.sinc(x)
        d = s - n
        #c = crappy_sinc(x)
        print("{} {:.15f} {:.15f} {}".format(x, s, n, d))
        x *= scale

