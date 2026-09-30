# Computer Graphics From Scratch

从零实现的光线追踪器（Ray Tracer），用纯 Python 渲染三维场景并输出 PPM 图像，带你一步步理解计算机图形学的核心管线。

## 特性

- **Whitted 式光线追踪**：从相机逐像素投射光线，解析求交。
- **光照模型**：环境光 + 漫反射 + Phong 镜面高光。
- **阴影**：对每个光源做遮挡检测（点光源 / 平行光）。
- **递归反射**：支持镜面反射物体的多次反弹（递归深度可配）。
- **零渲染依赖**：输出纯文本 P3 PPM，可直接用文本编辑器查看，无需 GUI 库。

## 项目结构

```
main.py            入口：构建场景（球体、光源、相机、视口）并触发渲染
Renderer.py        逐像素循环，串联各模块
RayTracer.py       求最近交点、光照计算、递归反射
Scene.py           场景（物体 + 光源 + 背景色）与最近交点求解
Sphere.py          球体解析求交
Camera.py          相机与画布→视口坐标换算
Viewport.py        视口尺寸与距离
Canvas.py          像素网格与 PPM 输出
Light/             AmbientLight / PointLight / DirectionalLight
Vec3.py / Point3.py / Ray.py / Color.py / Interval.py / Number.py   基础数学与数据类型
```

## 快速开始

环境要求：Python **>= 3.14**。推荐使用 [`uv`](https://github.com/astral-sh/uv) 管理依赖（项目已包含 `uv.lock`）。

```bash
# 1. 创建并激活虚拟环境（项目根目录下名称含 .venv / venv 的目录）
uv venv                 # 生成 .venv
source .venv/bin/activate

# 2. 安装依赖（mypy、numpy）
uv pip install -r <(uv pip compile pyproject.toml)   # 或直接：uv sync

# 3. 运行渲染
python main.py
```

运行后会在 `output/` 文件夹（脚本首次运行时自动创建）生成 `graph_sphere.ppm`。

## 查看结果

`output/graph_sphere.ppm` 是纯 ASCII 的 P3 PPM 文件，可直接用支持 PPM 的图像查看器打开，或用以下方式转成常见格式：

```bash
# 例如用 ImageMagick 转 PNG（需自行安装）
convert output/graph_sphere.ppm output/output.png
```

## 渲染流程详解

完整的调用流程图、模块职责对照表，以及光照 / 阴影 / 反射算法的说明，见 **[RenderingPipeline.md](./RenderingPipeline.md)**。

## 进度

* [x] Dedication
* [x] Acknowledgements
* [x] Table of Contents
* [x] Introduction
* [x] Introductory Concepts
* [x] Part I: Raytracing
  * [x] Basic Raytracing
  * [x] Light
  * [x] Shadows and Reflections
  * [x] Extending the Raytracer
* [ ] Part II: Rasterization
  * [x] Lines
  * [x] Filled Triangles
  * [x] Shaded Triangles
  * [x] Perspective Projection
  * [x] Describing and Rendering a Scene
  * [ ] Clipping
  * [ ] Hidden Surface Removal
  * [ ] Shading
  * [ ] Textures
  * [ ] Extending the Rasterizer
  * [ ] Appendixes
  * [ ] Linear Algebra
  * [ ] Afterword