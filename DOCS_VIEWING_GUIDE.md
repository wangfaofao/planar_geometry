# 📖 文档查看指南

这个指南说明如何查看项目的 Sphinx 文档，特别是如何验证数学公式的正确渲染。

## 🚀 快速开始

### 方法 1: 使用提供的脚本（推荐）

```bash
cd /home/wangheng/Desktop/planar_geometry

# 使用默认端口 8000
./scripts/serve_docs.sh

# 或使用自定义端口
./scripts/serve_docs.sh 8080
```

然后在浏览器中访问 `http://localhost:8000`

### 方法 2: 使用 Makefile

```bash
make serve-docs
```

### 方法 3: 手动启动服务器

```bash
cd docs/_build/html
.venv/bin/python -m http.server 8000
```

## 📊 文档结构

访问 `http://localhost:8000` 后，你会看到：

```
planar_geometry Documentation
│
├── 📘 User Guide (用户指南)
│   ├── Installation (安装)
│   ├── Quick Start (快速开始)
│   ├── Basic Usage (基础用法)
│   └── Advanced (高级主题)
│
├── 📕 API Reference (API 参考)
│   ├── Points (点)
│   ├── Vectors (向量)
│   ├── Lines (直线)
│   ├── Circles (圆)
│   ├── Polygons (多边形) ← 查看数学公式
│   └── Utils (工具函数) ← 查看公式
│
├── 🔧 Developer Guide (开发指南)
│   ├── Contributing (贡献指南)
│   └── Architecture (架构)
│
└── 🔍 Search (搜索)
```

## 🎓 查看数学公式

### Polygon.area() 方法

1. 在左侧导航栏点击 **"API Reference"** → **"Polygons"**
2. 找到 **"Polygon.area()"** 部分
3. 你会看到正确的 LaTeX 数学公式：

$$A = \frac{1}{2} \left| \sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i) \right|$$

### circle_line_intersection() 函数

1. 在左侧导航栏点击 **"API Reference"** → **"Utils"**
2. 找到 **"intersection_ops"** 部分
3. 查看 **"circle_line_intersection()"** 函数
4. 你会看到距离公式：

$$d = \frac{|ax + by + c|}{\sqrt{a^2 + b^2}}$$

### cartesian_to_polar() 函数

1. 在左侧导航栏点击 **"API Reference"** → **"Utils"**
2. 找到 **"coordinate_ops"** 部分
3. 查看 **"cartesian_to_polar()"** 函数
4. 你会看到向量表示的算法说明

## 🔧 故障排除

### 错误: "address already in use"

**问题**: 端口已被占用

**解决方案**:
```bash
# 使用不同的端口
./scripts/serve_docs.sh 8001
./scripts/serve_docs.sh 8002
./scripts/serve_docs.sh 9999
```

或者找到占用该端口的进程并杀死它：
```bash
# 查找占用端口的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>
```

### 错误: "文档目录不存在"

**问题**: 文档还未生成

**解决方案**:
```bash
# 生成文档
make docs

# 或手动生成
.venv/bin/sphinx-build -b html docs docs/_build/html
```

### 错误: "虚拟环境 Python 不存在"

**问题**: 虚拟环境不存在

**解决方案**:
```bash
# 使用 uv 创建虚拟环境（推荐）
uv venv

# 或使用 venv
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
```

### 公式未正确渲染

**原因**: 可能是浏览器缓存

**解决方案**:
1. 硬刷新浏览器：`Ctrl+Shift+R` (Linux/Windows) 或 `Cmd+Shift+R` (Mac)
2. 清除浏览器缓存
3. 使用无痕/隐私浏览模式
4. 尝试其他浏览器

## 📝 文档生成

### 重新生成文档

修改源代码或文档后，重新生成：

```bash
# 使用 Makefile（推荐）
make docs

# 或直接使用 sphinx-build
.venv/bin/sphinx-build -b html docs docs/_build/html

# 清除缓存后重新生成
rm -rf docs/_build
make docs
```

### 生成其他格式

```bash
# 生成 PDF
make pdf

# 生成 ePub
make epub

# 生成纯文本
make text
```

## 🌐 在线访问

如果文档已部署到 ReadTheDocs：

- **稳定版本**: https://planar-geometry.readthedocs.io/en/stable/
- **开发版本**: https://planar-geometry.readthedocs.io/en/latest/

## 📱 移动设备

文档支持响应式设计，可在移动设备上查看：

1. 获取你的本地 IP 地址：
```bash
# Linux/Mac
ifconfig | grep "inet "

# Windows
ipconfig
```

2. 在移动设备上访问：
```
http://<your-ip>:8000
```

## 💡 快速命令参考

```bash
# 查看文档
./scripts/serve_docs.sh

# 生成文档
make docs

# 生成并查看
make serve-docs

# 清除文档缓存
rm -rf docs/_build

# 检查文档警告
.venv/bin/sphinx-build -b html docs docs/_build/html 2>&1 | grep WARNING
```

## 🎯 下一步

查看完文档后，你可以：

1. ✅ **理解项目架构** - 阅读 "Architecture" 页面
2. ✅ **学习基础用法** - 跟随 "Quick Start" 教程
3. ✅ **查看 API 参考** - 浏览所有可用的类和函数
4. ✅ **为项目做贡献** - 查看 "Contributing" 指南

## 📞 支持

如果文档有任何问题或建议，请：

1. 查看 GitHub Issues: https://github.com/wangheng/planar_geometry/issues
2. 提交 Pull Request: https://github.com/wangheng/planar_geometry/pulls
3. 查看 Contributing 指南

---

**最后更新**: 2026-02-01
**文档版本**: 0.2.0
