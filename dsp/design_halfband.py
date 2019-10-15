
# From: https://www.dsprelated.com/showcode/270.php
import numpy
from numpy import log10, abs, pi
import scipy
from scipy import signal
import matplotlib
import matplotlib.pyplot
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import math

# # ~~[Filter Design with Parks-McClellan Remez]~~
# N = 32  # Filter order
# # Filter symetric around 0.25 (where .5 is pi or Fs/2)
# bands = numpy.array([0., .22, .28, .5])
# h = signal.remez(N+1, bands, [1,0], [1,1])
# h[abs(h) <= 1e-4] = 0.
# (w,H) = signal.freqz(h)
#
# # ~~[Filter Design with Windowed freq]~~
# b = signal.firwin(N+1, 0.5)
# b[abs(h) <= 1e-4] = 0.
# (wb, Hb) = signal.freqz(b)
#
# # Dump the coefficients for comparison and verification
# print('          remez       firwin')
# print('------------------------------------')
# for ii in range(N+1):
#     print(' tap %2d   %-3.6f    %-3.6f' % (ii, h[ii], b[ii]))
#
# ## ~~[Plotting]~~
# # Note: the pylab functions can be used to create plots,
# #       and these might be easier for beginners or more familiar
# #       for Matlab users.  pylab is a wrapper around lower-level
# #       MPL artist (pyplot) functions.
# #fig = mpl.pyplot.plot()
# #ax0 = fig.add_subplot(211)
# plt.stem(numpy.arange(len(h)), h)
# plt.grid(True)
# plt.title('Parks-McClellan (remez) Impulse Response')
# #ax1 = fig.add_subplot(212)
# #ax1.stem(numpy.arange(len(b)), b)
# #ax1.set_title('Windowed Frequency Sampling (firwin) Impulse Response')
# #ax1.grid(True)
# plt.show()
#
# #fig.savefig('hb_imp.png')
#
# fig = mpl.pyplot.figure()
# ax1 = fig.add_subplot(111)
# ax1.plot(w, 20*log10(abs(H)))
# ax1.plot(w, 20*log10(abs(Hb)))
# ax1.legend(['remez', 'firwin'])
# bx = bands*2*pi
# ax1.axvspan(bx[1], bx[2], facecolor='0.5', alpha='0.33')
# ax1.plot(pi/2, -6, 'go')
# ax1.axvline(pi/2, color='g', linestyle='--')
# ax1.axis([0,pi,-64,3])
# ax1.grid('on')
# ax1.set_ylabel('Magnitude (dB)')
# ax1.set_xlabel('Normalized Frequency (radians)')
# ax1.set_title('Half Band Filter Frequency Response')
#fig.savefig('hb_rsp.png')

def plot_frequency_response(b):
    (w, H) = signal.freqz(b)
    bands = numpy.array([0., .22, .28, .5])
    plt.plot(w, 20 * log10(abs(H)))
    bx = bands * 2 * pi
    plt.axvspan(bx[1], bx[2], facecolor='0.5', alpha=0.33)
    #plt.axvspan(bx[1], bx[2])
    plt.plot(pi / 2, -6, 'go')
    plt.axvline(pi / 2, color='g', linestyle='--')
    plt.axis([0, pi, -104, 3])

    plt.grid('on')
    plt.ylabel('Magnitude (dB)')
    plt.xlabel('Normalized Frequency (radians)')
    plt.title('Half Band Filter Frequency Response')
    # fig.savefig('hb_rsp.png')
    plt.show()

def windowed_halfband(N):
    # ~~[Filter Design with Windowed freq]~~
    b = signal.firwin(N + 1, 0.5)
    b[abs(b) <= 1e-4] = 0.0
    return b

def remez_halfband(N):
    # ~~[Filter Design with Windowed freq]~~
    bands = numpy.array([0., .22, .28, .5])
    b = signal.remez(N+1, bands, [1,0], [1,1])
    b[abs(b) <= 1e-4] = 0.0
    return b

def sinc_halfband(N):
    r = list(range(-N//2, N//2 + 1))
    r = [x * 0.5 for x in r]
    b = np.sinc(r)
    k = list(np.kaiser(len(b), 9.0))
    b = [a * b for a,b in zip(b, k)]
    b = [x * 0.5 for x in b]
    b = [x if abs(x) > 1e-10 else 0.0 for x in b]
    return b

if __name__ == '__main__':
    num_taps = 100
    b = sinc_halfband(num_taps)
    print (b)
    plot_frequency_response(b)