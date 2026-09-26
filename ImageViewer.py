"""
图片查看工具：保存后用系统默认程序自动打开图片。

封装为 ImageViewer.open_image(path)，按当前操作系统选择对应的打开命令，
便于在多个绘图脚本中复用，无需重复平台判断逻辑。
"""

import os
import subprocess
import sys


class ImageViewer:
    """调用系统默认查看器打开图片的静态工具类。"""

    @staticmethod
    def open_image(path: str) -> None:
        """用系统默认程序打开给定路径的图片。

        path：图片文件的路径（如 "graph_line_no_interpolation.png"）。
        按平台分别使用 open（macOS）/ startfile（Windows）/ xdg-open（Linux）。
        """
        if sys.platform == "darwin":
            subprocess.run(["open", path])
        elif sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "linux":
            subprocess.run(["xdg-open", path])
