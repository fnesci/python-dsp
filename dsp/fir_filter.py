# FIR filter

class FirFilter:
    def __init__(self, b):
        self.__b = b
        self.__N = len(b)
        self.__N_minus_1 = self.__N - 1
        self.__history = [0] * self.__N
        self.__head = 0

    def N(self):
        return self.__N

    def next(self, x):
        self.__history[self.__head] = x

        y = 0.0
        k = 0
        for i in range(self.__head, self.__N):
            y += self.__b[k] * self.__history[i]
            k += 1

        for i in range(0, self.__head):
            y += self.__b[k] * self.__history[i]
            k += 1

        self.__head -= 1
        if self.__head < 0:
            self.__head = self.__N_minus_1

        return y

    def block_next(self, xs, ys):
        for x in xs:
            self.__history[self.__head] = x

            y = 0.0
            k = 0
            for i in range(self.__head, self.__N):
                y += self.__b[k] * self.__history[i]
                k +=1

            for i in range(0, self.__head):
                y += self.__b[k] * self.__history[i]
                k +=1

            self.__head -= 1
            if self.__head < 0:
                self.__head = self.__N_minus_1

            ys.append(y)
