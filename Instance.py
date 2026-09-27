from dataclasses import dataclass

from geometry.Model import Model
from geometry.Vec3 import Vec3


@dataclass
class Instance:
    model: Model
    position: Vec3
