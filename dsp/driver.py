import math
import scipy
import scipy.signal
import sinc_resampler
import wf
import matplotlib.pyplot as plt
import numpy as np

def plot_frequency_response(rs):

    f = []
    for i in range(rs.settings.FilterLength):
        n = i - rs.settings.WingLength
        f.append(rs.filter(n))
        pass

    w, h = scipy.signal.freqz(f, worN=2048)
    fig = plt.figure()
    plt.title('Digital filter frequency response')
    ax1 = fig.add_subplot(111)

    plt.plot(w, 20 * np.log10(abs(h)), 'b')
    plt.ylabel('Amplitude [dB]', color='b')
    plt.xlabel('Frequency [rad/sample]')

    ax2 = ax1.twinx()
    angles = np.unwrap(np.angle(h))
    plt.plot(w, angles, 'g')
    plt.ylabel('Angle (radians)', color='g')
    plt.grid()
    plt.axis('tight')
    plt.show()

def create_data(N, centers):
    samples = []

    for n in range(N):
        x = 0.0
        for f in centers:
            x += math.cos(f * n)
        samples.append(x)
    return samples

def test_resampler(resamp):
    in_length = 4096
    in_frequencies = [0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5,
                      1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.13]
    in_data = create_data(in_length, in_frequencies)

    print("Num frequencies in the test data: {}".format(len(in_frequencies)))

    #in_data = create_data(in_length, [0.8 * math.pi])
    #print in_data[:16]

    fft_in_data = 20.0 * np.log10(np.abs(np.fft.fft(in_data)))
    print(len(in_data), len(np.fft.fft(in_data)))
    resamp.add_samples(in_data)
    out_data = resamp.resample()
    fft_out_data = 20.0 * np.log10(np.abs(np.fft.fft(out_data)))

    #expected_data = create_data(len(out_data), [1.6 * math.pi])

    print(len(out_data), len(np.fft.fft(fft_out_data)))
    plt.plot(
        np.linspace(0, 1.0, len(fft_in_data), endpoint=False), fft_in_data
        ,
        np.linspace(0, 1.0, len(fft_out_data), endpoint=False), fft_out_data
        )
    plt.grid()
    plt.show()
    # plt.plot(
    #     np.linspace(0, 1.0, len(in_data), endpoint=False), in_data
    #     ,
    #     np.linspace(0, 1.0, len(out_data), endpoint=False), out_data
    #     ,
    #     np.linspace(0, 1.0, len(expected_data), endpoint=False), expected_data
    #     )
    plt.show()
    print(len(out_data))


if __name__ == '__main__':
    filter_len = 200
    table_entries_per_zero_crossing = 200

    ratio = 0.33333333333333333333333333
    resamp = sinc_resampler.SincResampler(ratio, filter_len, wf.blackman_harris, table_entries_per_zero_crossing)
    test_resampler(resamp)
    plot_frequency_response(resamp)

    # resamp = sinc_resampler.SincResampler(ratio, filter%_length, wf.triangular)
    # filter = [resamp.h(n) for n in range(resamp.filter_length)]
    # print filter
    # plot_frequency_response(filter)
    #
    # resamp = sinc_resampler.SincResampler(ratio, filter_length, wf.hann)
    # filter = [resamp.h(n) for n in range(resamp.filter_length)]
    # print filter
    # plot_frequency_response(filter)
    #
    # resamp = sinc_resampler.SincResampler(ratio, filter_length, wf.hamming)
    # filter = [resamp.h(n) for n in range(resamp.filter_length)]
    # print filter
    # plot_frequency_response(filter)
    #
    # resamp = sinc_resampler.SincResampler(ratio, filter_length, wf.blackman_harris)
    # filter = [resamp.h(n) for n in range(resamp.filter_length)]
    # print filter
    # plot_frequency_response(filter)


