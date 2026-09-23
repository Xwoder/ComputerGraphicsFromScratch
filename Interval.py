from dataclasses import dataclass

from Number import Number


@dataclass
class Interval:
    min: Number
    max: Number

    def __contains__(self, value: Number) -> bool:
        return self.min <= value <= self.max
