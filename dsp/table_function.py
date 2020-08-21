import math

class TableFunction:
    class TableEntry:
        def __init__(self, x0, x1, y0, y1):
            self.x0 = x0
            self.x1 = x1
            self.y0 = y0
            self.y1 = y1
            self.m = (y1 - y0) / (x1 - x0)
            self.b = y0 - self.m * x0

            # _y0 = self.m * x0 + self.b
            # assert math.fabs(y0 - _y0) < 1e-12
            # _y1 = self.m * x1 + self.b
            # assert math.fabs(y1 - _y1) < 1e-12
            # pass

    def __init__(self, f, min_x, max_x, num_samples):
        self.min_x = float(min_x)
        self.max_x = float(max_x)
        self.left_y = f(min_x)
        self.right_y = f(max_x)
        self.num_samples = num_samples
        self.delta_x = max_x - min_x
        self.index_scale = (self.num_samples) / self.delta_x
        self.step_size = 1.0 / (num_samples)
        self.entries = []

        x1 = min_x
        y1 = f(min_x)
        for i in range(num_samples):
            x0 = x1
            y0 = y1
            x1 = min_x + self.step_size * self.delta_x * float(i + 1)
            y1  = f(x1)
            entry = TableFunction.TableEntry(x0, x1, y0, y1)
            self.entries.append(entry)
            # print ("x0: {}, x1: {}, m: {}, b: {}".format(entry.x0, entry.x1, entry.m, entry.b))

    def evaluate(self, x):
        """

        :param x:
        :return:
        """
        index = int(self.index_scale * (x - self.min_x))
        if index < 0:
            return self.left_y
        elif index >= len(self.entries):
            return self.right_y
        else:
            entry = self.entries[index]
            #if not(x >= entry.x0 and x < entry.x1):
            #    print("")

            y = entry.m * x + entry.b
            return y


    # These methods let one start a starting point and a step size
    # and then generate values slightly more efficiently than
    # def setup_eval(self, start_x, step_size):
    #     pass
    #
    # def next_eval(self):
    #     pass


# TODO: Future variations:
#  EventTableFunction
#  OddTableFunction
#  Sin
#  Cos

if __name__ == '__main__':
    from sinc import sinc
    import math

    f = lambda x: sinc(x, math.pi, 1.0)
    table = TableFunction(f, -2 * math.pi, 2.0 * math.pi, 10000)

    x = -5.0
    x_step = 0.07
    while x < 5.0:
        r = f(x)
        t = table.evaluate(x)
        d = t - r
        print("{:.15f} {:.15f} {:.15f} {:.15f}".format(x, r, t, d))
        x += x_step

    t = table.evaluate(-1e6)
    print("{:.15f} {:.15f}".format(-1e6, t))
    t = table.evaluate(1e6)
    print("{:.15f} {:.15f}".format(1e6, t))
