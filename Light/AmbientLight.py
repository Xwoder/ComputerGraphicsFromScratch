from Light.Light import Light


class AmbientLight(Light):
    """环境光：均匀照亮整个场景、无方向，仅提供全局基础亮度（强度由 intensity 给出）。"""