import numpy as np
from numpy.random import Generator

from Number import Number
from Vec3 import Vec3

_rng: Generator = np.random.Generator(np.random.MT19937())


def random_number(
        min: Number = 0.0,
        max: Number = 1.0) -> Number:
    """Returns a random real in [min, max)."""
    return float(min + (max - min) * _rng.random())


def random_in_unit_disk() -> Vec3:
    """Returns a random point inside the unit disk (z = 0)."""

    while True:
        p = Vec3(x=random_number(-1, 1), y=random_number(-1, 1), z=0)
        if p.length_squared() < 1:
            return p
