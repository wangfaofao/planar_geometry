# planar_geometry 文档

## 快速开始

### 查看本地文档

```bash
# 方法1：使用Python的http.server
cd docs/_build/html
python3 -m http.server 8000

# 然后在浏览器打开: http://localhost:8000
```

### 重新生成文档

```bash
# 使用Makefile（推荐）
cd /home/wangheng/Desktop/planar_geometry
make docs

# 或者直接使用sphinx-build
sphinx-build -b html docs docs/_build/html
```

## 文档结构

```
docs/
├── conf.py                    # Sphinx配置文件
├── index.rst                  # 主索引文件
├── guide/                     # 用户指南
│   ├── installation.rst       # 安装指南
│   ├── quick_start.rst        # 快速开始
│   ├── basic_usage.rst        # 基础用法
│   └── advanced.rst           # 高级用法
├── api/                       # API参考
│   ├── points.rst             # 点API
│   ├── vectors.rst            # 向量API
│   ├── lines.rst              # 线API
│   ├── circles.rst            # 圆API
│   ├── polygons.rst           # 多边形API
│   └── utils.rst              # 工具函数API
├── dev/                       # 开发文档
│   ├── contributing.rst       # 贡献指南
│   └── architecture.rst       # 架构设计
└── _build/html/               # 生成的HTML文档（此目录）
```

## 文档内容

### 用户指南
- **安装指南** - 如何安装planar_geometry
- **快速开始** - 基本示例和Hello World
- **基础用法** - 常见操作和用法
- **高级用法** - 几何变换、交点检测、复杂操作

### API参考
- **Points API** - Point2D类的完整API文档
- **Vectors API** - Vector2D类的完整API文档  
- **Lines API** - Line和LineSegment类的完整API文档
- **Circles API** - Circle和Ellipse类的完整API文档
- **Polygons API** - Polygon、Triangle、Rectangle类的完整API文档
- **Utilities API** - 所有工具函数的完整API文档

### 开发文档
- **贡献指南** - 如何为项目贡献代码
- **架构设计** - 项目架构和设计原则

## 生成的HTML文档

所有HTML文档位于 `docs/_build/html/` 目录：

- `index.html` - 主页
- `api/` - API参考文档
- `guide/` - 用户指南
- `dev/` - 开发文档
- `genindex.html` - 索引
- `py-modindex.html` - Python模块索引
- `search.html` - 搜索页面

## 主题

文档使用 **Sphinx Read the Docs (RTD)** 主题，具有以下特点：
- 响应式设计（支持移动设备）
- 深色/浅色主题切换
- 搜索功能
- 版本切换（未来配置）
- 右侧导航栏
- 顶部导航栏

## 特性

✅ **自动文档** - 从Python docstrings自动生成  
✅ **代码高亮** - Python代码语法高亮  
✅ **类型提示** - 显示函数参数和返回类型  
✅ **交叉引用** - 类、函数、模块之间的链接  
✅ **搜索** - 全文搜索功能  
✅ **导出** - 支持导出为PDF（需额外配置）

## 配置

Sphinx配置文件：`docs/conf.py`

关键配置：
- 主题：`sphinx_rtd_theme`
- 语言：`en` (English)
- 自动文档扩展：`autodoc`
- 类型提示支持：`sphinx_autodoc_typehints`
- Napoleon (Google风格docstrings)

## 常见问题

### Q: 文档无法生成？
A: 确保安装了所有必要的依赖：
```bash
uv pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints
```

### Q: 如何添加新的文档页面？
A: 
1. 在对应的目录下创建`.rst`文件
2. 在`index.rst`的`toctree`中添加引用
3. 重新生成文档

### Q: 如何修改主题样式？
A: 编辑`docs/conf.py`中的`html_theme_options`

## 更新文档

### 更新指南
编辑相应的`.rst`文件，然后重新生成文档。

### 更新API文档
API文档从源代码的docstrings自动生成，修改源代码中的docstrings后重新生成即可。

## 发布文档

### 部署到ReadTheDocs
1. 将项目推送到GitHub
2. 连接GitHub到ReadTheDocs
3. ReadTheDocs会自动构建文档

### 部署到GitHub Pages
1. 构建文档：`make docs`
2. 将`docs/_build/html`推送到gh-pages分支
3. GitHub会自动发布

## 更多信息

- [Sphinx官方文档](https://www.sphinx-doc.org/)
- [Sphinx RTD主题](https://sphinx-rtd-theme.readthedocs.io/)
- [reStructuredText指南](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)

---

**最后更新**: 2026-02-01
