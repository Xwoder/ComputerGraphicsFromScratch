import math
from dataclasses import dataclass

from Number import Number


@dataclass
class Interval:
    min: Number
    max: Number

    def __contains__(self, value: Number) -> bool:
        # 排除正/负无穷：避免 `math.inf in Interval(t_min, math.inf)` 因
        # `inf <= inf` 成立而误判为命中；未命中时 `intersect` 返回 (inf, inf)
        # 应当被任何区间过滤掉，而非依赖调用方 `t < closest_t` 兜底。
        return not math.isinf(value) and self.min <= value <= self.max
