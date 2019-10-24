import math
import cmath

def get_filter(fc, fs, N):
    T = 1.0 / fs
    w = 2 * math.pi * fc
    phase = -0.5 * (N - 1.0) * w * T
    phase = 0.0
    h = []
    for n in range(N):
        h.append(cmath.exp(1j*(w * n * T + phase)))

    return h

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import scipy.signal
    import numpy as np

    def plot_filter_response(b):
        w, h = scipy.signal.freqz(b)

        fig, ax1 = plt.subplots()
        ax1.set_title('Digital filter frequency response')
        ax1.plot(w, 20 * np.log10(abs(h)), 'b')
        ax1.set_ylabel('Amplitude [dB]', color='b')
        ax1.set_xlabel('Frequency [rad/sample]')
        ax2 = ax1.twinx()
        angles = np.unwrap(np.angle(h))
        ax2.plot(w, angles, 'g')
        ax2.set_ylabel('Angle (radians)', color='g')
        ax2.grid()
        ax2.axis('tight')
        plt.show()

    b = get_filter(500.0,44000.0, int(44000.0 / 1200))
    plot_filter_response(b)