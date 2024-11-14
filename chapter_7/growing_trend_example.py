import numpy as np


def growing_avg(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1 :] / n


def is_growing(data):
    return np.all(np.diff(growing_avg(np.array(data), n=4)) > 0)


rates_1 = [3.0, 6.0, 10.0, 4.2, 11.0]
rates_2 = [6.0, 4.0, 5.0, 4.0, 3.2]

print("Is growing trend: ", is_growing(rates_1))
print("Is growing trend: ", is_growing(rates_2))
