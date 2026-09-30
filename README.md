# Computer Graphics From Scratch

用纯 Python 从零实现的计算机图形学练习项目，对照 Gabriel Gambetta《Computer Graphics from Scratch》一书，**同时实现两套渲染管线**，均输出 PPM / PNG 图像，无第三方渲染依赖：

- **光线追踪（Ray Tracing）**：从相机逐像素投射光线，解析求交、光照、阴影与递归反射。
- **网格栅格化（Rasterization）**：把「顶点 + 三角面」描述的 3D 网格透视投影到画布，逐三角面绘制（线框 + 插值着色）。

## 特性

光线追踪：

- **Whitted 式光线追踪**：从相机逐像素投射光线，解析求交。
- **光照模型**：环境光 + 漫反射 + Phong 镜面高光。
- **阴影**：对每个光源做遮挡检测（点光源 / 平行光）。
- **递归反射**：支持镜面反射物体的多次反弹（递归深度可配，默认 3）。

栅格化：

- **透视投影**：`Camera.projectVertex` 把相机空间顶点投到画布像素。
- **网格绘制**：`Model`（顶点 + 三角面）逐三角面线框绘制，三角面自带颜色。
- **实例化（Instancing）**：`Instance` 把同一 `Model` 以不同变换摆放到世界空间，复用网格。
- **基础图元**：直线（Bresenham / 对称插值）、填充三角形、插值着色三角形。

通用：

- **零渲染依赖**：输出纯文本 P3 PPM（光追 / 线框）或 Pillow 渲染的 PNG（2D 图元练习）。
- **相机矩阵**：`Camera.make_camera_matrix` 合成世界→相机视图矩阵，支持相机平移 / 旋转。

## 项目结构

```
examples/                  所有可运行示例（见下方「快速上手」）
  main_draw_sphere.py      光线追踪：四球场景 → output/graph_sphere.ppm
  main_draw_cube.py        栅格化：单立方体线框 → output/graph_cube.ppm
  main_draw_two_cubes.py   栅格化：两个实例化立方体 → output/main_draw_two_cubes.ppm
  main_draw_line_naive.py  2D：朴素（按列最邻近）直线栅格化 → output/graph_line_no_interpolation.png
  main_draw_line_interpolation.py  2D：对称插值直线栅格化 → output/graph_line_with_interpolation.png
  main_draw_triangle.py    2D：线框 + 填充三角形 → output/graph_triangle.png
  main_draw_shaded_triangle.py     2D：插值着色三角形 → output/graph_shaded_triangle.png

# ── 渲染器与场景 ──
Renderer.py                统一渲染器：render() 光线追踪 / render_scene() 栅格化实例
Rasterizer.py              Rasterizer + PixelWriter：renderObject / renderTriangle / 线框三角面
RayTracer.py               求最近交点、光照计算、compute_lighting、递归反射
RayTracingScene.py         光追场景（spheres + lights + 背景色）与 closestIntersection
RasterizationScene.py      栅格化场景（instances + 背景色）

# ── 核心数据类型与数学 ──
Camera.py                  相机：origin/rotation/translation；canvasToViewport / projectVertex / make_camera_matrix
Viewport.py                视口：width/height/distance
Canvas.py                  3D 像素缓冲 + savePPM + draw_line（Bresenham 整数直线）
Canvas2D.py                2D 像素缓冲 + draw_line（对称插值）/ fill_triangle_scanlines / draw_shaded_triangle
Sphere.py                  球体解析求交（intersect）
Ray.py                     光线（origin + direction，at(t) 求交点）
Interval.py                有效 t 区间判定，自动排除 ±inf
Number.py                  浮点数值类型别名
Transform.py / Rotation.py 实例变换（缩放→旋转→平移）与欧拉角
Instance.py                模型实例（model + transform）
Line2ByTwoPoints.py        由两点定义的 2D 直线
ImageViewer.py             跨平台打开生成的图像
PlotUtils.py               2D 图元练习的栅格 / 坐标轴 / 字体辅助

geometry/                  向量与矩阵：Vec3、Point2、Point3、Matrix、Matrix4、Triangle、RotationMatrix
color/Color.py             Color / BLACK / WHITE 等：RGB 分量、按标量缩放（截断 0~255）、叠加
light/                     Light 基类 + AmbientLight / PointLight / DirectionalLight
model/Model.py             Model：顶点 + 三角面；create_cube() 便捷构建立方体
```

## 快速上手

环境要求：Python **>= 3.14**。推荐使用 [`uv`](https://github.com/astral-sh/uv) 管理依赖（项目已包含 `uv.lock`）。

```bash
# 1. 创建并激活虚拟环境（项目根目录下名称含 .venv / venv 的目录）
uv venv                 # 生成 .venv
source .venv/bin/activate

# 2. 安装依赖（mypy、numpy、pillow）
uv sync                 # 或：uv pip install -r <(uv pip compile pyproject.toml)

# 3. 运行示例（在项目根目录下执行，脚本会把结果写到 output/）
python examples/main_draw_sphere.py          # 光线追踪：四球
python examples/main_draw_two_cubes.py       # 栅格化：两个实例化立方体
python examples/main_draw_cube.py            # 栅格化：单立方体线框
python examples/main_draw_triangle.py        # 2D：线框 + 填充三角形
python examples/main_draw_shaded_triangle.py # 2D：插值着色三角形
python examples/main_draw_line_interpolation.py  # 2D：对称插值直线
python examples/main_draw_line_naive.py     # 2D：朴素最邻近直线
```

每个脚本都会自动创建 `output/` 目录并把图像写入其中，部分脚本还会用系统默认查看器打开结果。

## 查看结果

- **PPM**（光追与线框立方体）：`output/*.ppm` 是纯 ASCII 的 P3 PPM 文件，可直接用支持 PPM 的图像查看器打开，或用 ImageMagick 等工具转成常见格式：

  ```bash
  convert output/graph_sphere.ppm output/output.png   # 需自行安装 ImageMagick
  ```

- **PNG**（2D 图元练习）：`output/*.png` 由 Pillow 生成，可直接打开。

## 渲染流程详解

- **光线追踪**：完整的调用流程图、模块职责对照表，以及光照 / 阴影 / 反射算法的说明，见 **[RenderingPipeline.md](./RenderingPipeline.md)**。
- **网格栅格化**：`Renderer.render_scene()` 对齐书中 `RenderScene()` 伪代码——先 `MakeCameraMatrix(camera)` 得世界→相机矩阵 `M_camera`，对每个实例合成 `M = M_camera · I.transform`，再把模型顶点一次性变换到相机空间后 `ProjectVertex` 透视投影，最后逐三角面 `DrawWireframeTriangle` 连出三条边。关键模块：`Camera.make_camera_matrix` / `Camera.projectVertex`、`Model` / `Triangle` / `Instance`、`Rasterizer.draw_wireframe_triangle`（`Rasterizer.py`）。

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
