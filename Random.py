import numpy as np
from numpy.random import Generator

from Number import Number

_rng: Generator = np.random.Generator(np.random.MT19937())


def random_number(
        min: Number = 0.0,
        max: Number = 1.0) -> Number:
    """Returns a random real in [min, max)."""
    return float(min + (max - min) * _rng.random())
