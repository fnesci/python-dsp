import bitarray

class GardnerLoop:
    def __init__(self, samples_per_symbol, gain = 1.0):
        self.samples_per_symbol = samples_per_symbol
        self.middle = samples_per_symbol // 2
        self.end = samples_per_symbol - 1
        self.history = []
        self.next_symbol = float(samples_per_symbol)
        self.last_symbol = 0
        self.gain = gain

    def add_samples(self, samples):
        self.history.extend(samples)
        e = []
        s = []
        bits = bitarray.bitarray()

        while round(self.next_symbol) < len(self.history):
            symbol_index = int(round(self.next_symbol))
            bit = 1 if self.history[symbol_index] < 0.0 else 0

            error = self.gain * (self.history[symbol_index] - self.history[symbol_index - self.samples_per_symbol]) * \
                    self.history[symbol_index - self.middle]
            self.next_symbol += self.samples_per_symbol - error
            samples_between = symbol_index - self.last_symbol
            self.last_symbol = symbol_index

            e.extend([error] * samples_between)
            s.extend([2.0 * bit - 1.0] * samples_between)
            bits.append(bit)

        self.history = self.history[self.last_symbol:]
        self.next_symbol -= self.last_symbol

        return bits, (s, e)

