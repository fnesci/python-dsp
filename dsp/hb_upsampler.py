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

        self.compressed_filter = [0] * M

        m0 = 0
        m1 = M - 1
        for l in range(L):
            if not zero:
                self.compressed_filter[m0] = hb_filter[l]
                self.compressed_filter[m1] = hb_filter[l]
                m0 += 1
                m1 -= 1
            zero = not zero

        assert(m0 == m1)
        self.compressed_filter[m0] = hb_filter[L]
        pass
