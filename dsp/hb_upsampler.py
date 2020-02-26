import hb_filters

# This class implements an upsampler that increases the input sample rate by 2

class HbUpsampler:
    """
    This class creates a 2x upsampler.  If no filter is specified, then the default
    HB filter is used.  If a filter is supplied it needs to have zeros in the
    usual places
    """

    def __init__(self, hb_filter=None):
        pass
        if hb_filter is None:
            hb_filter = hb_filter.default_hb

        # Type == 1: zeros starting at index 0
        # Type == 3: zeros starting at index 1
        hb_type = len(hb_filter) % 4
        assert(hb_type == 1 or hb_type == 3)
        zero = False if hb_type == 3 else True
        L = len(hb_filter) // 2
        M = 3 + (len(hb_filter) - 3) // 2
        if hb_type == 1:
            M -= 1

        self.compressed_filter = [0] * (M - 1)

        m0 = 0
        m1 = M - 2
        for l in range(L):
            if not zero:
                self.compressed_filter[m0] = hb_filter[l]
                self.compressed_filter[m1] = hb_filter[l]
                m0 += 1
                m1 -= 1
            zero = not zero

        self.sample_to_scale = L
        self.sample_scale = hb_filter[L]

        self.__N = len(self.compressed_filter)
        self.__N_minus_1 = self.__N - 1
        self.__history = [0] * self.__N
        self.__head = 0
        self.__scaled_sample_index = self.__N // 2

    """
    x3      b0
    0       0
    x2      b2
    0       b3
    x1      b4
    0       0
    x0      b6

    push 0      

    0       b0
    x3      0
    0       b2
    x2      b3
    0       b4
    x1      0
    0       b6

    push X4
    x4      b0
    0       0
    x3      b2
    0       b3
    x2      b4
    0       0
    x1      b6

    """

    def block_next(self, xs, ys):
        for x in xs:
            self.__history[self.__head] = x

            y = 0.0
            k = 0
            for i in range(self.__head, self.__N):
                y += self.compressed_filter[k] * self.__history[i]
                k +=1

            for i in range(0, self.__head):
                y += self.compressed_filter[k] * self.__history[i]
                k +=1

            self.__head -= 1
            if self.__head < 0:
                self.__head = self.__N_minus_1

            self.__scaled_sample_index -= 1
            if self.__scaled_sample_index < 0:
                self.__scaled_sample_index = self.__N_minus_1

            ys.append(y)
            ys.append(self.sample_scale * self.__history[self.__scaled_sample_index])

