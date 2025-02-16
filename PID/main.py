import numpy as np
import matplotlib.pyplot as plt


class PID:

    def __init__(self, k_p, k_i, k_d):
        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_d

        self.se = 0
        self.le = None

    def control(self, err):
        u = self.k_p * err
        u += self.k_i * (self.se + err)
        u += self.k_d * ((err - self.le) if self.le is not None else 0)

        self.se += err
        self.le = err

        return u


class CaseA:

    def __init__(self, pid):
        self.expected = 1
        self.actual = 0.2
        self.pid = pid

    def control(self):
        err = self.expected - self.actual
        u = self.pid.control(err)
        self.actual += u
        return self.actual


class CaseB:

    def __init__(self, pid):
        self.expected = 1
        self.actual = 0.2
        self.pid = pid

    def control(self):
        err = self.expected - self.actual
        u = self.pid.control(err)
        self.actual += u
        self.actual -= 0.1
        return self.actual


if __name__ == "__main__":
    pid = PID(0.5, 0.5, 0.5)
    c = CaseB(pid)

    x = [0] + [_ + 1 for _ in range(100)]
    y = [0.2] + [c.control() for _ in range(100)]

    plt.xlim(0)
    plt.xticks(np.arange(0, 120, 20))
    plt.ylim(0)
    plt.yticks(np.arange(0, 2, 0.2))
    plt.axhline(y=1, color='r', linestyle=':')
    plt.plot(x, y)
    plt.show()
