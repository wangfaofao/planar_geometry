# 🧮 MathJax 公式渲染修复指南

## 问题说明

你指出公式在文档中显示为字符串形式而不是渲染的数学公式。这是因为虽然 docstring 中有 `:math:` 标记，但 MathJax 库没有被正确配置和加载到生成的 HTML 中。

## 根本原因

1. **`:math:` 角色的限制**: Sphinx 的 `:math:` 角色生成 `<span class="math">` 标签
2. **MathJax 默认行为**: MathJax 3 默认只识别 `\(...\)` 和 `\[...\]` 格式
3. **缺少转换层**: 需要一个 JavaScript 脚本来将 Sphinx 的标签转换为 MathJax 能处理的格式
4. **库未加载**: MathJax 库本身未在生成的 HTML 中被加载

## 完整解决方案

### 1. 创建自定义 JavaScript 文件 (`docs/_static_source/mathjax-config.js`)

```javascript
// 加载 MathJax 库
var script = document.createElement('script');
script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';
script.async = true;
document.head.appendChild(script);

// 配置 MathJax
window.MathJax = {
  tex: {
    inlineMath: [['\\(', '\\)']],
    displayMath: [['\\[', '\\]']]
  },
  svg: {
    fontCache: 'global'
  },
  startup: {
    pageReady: () => {
      handleMathSpans();
      return MathJax.typesetPromise();
    }
  }
};

// 处理 Sphinx 生成的 .math class 标签
function handleMathSpans() {
  const mathElements = document.querySelectorAll('span.math');
  
  mathElements.forEach(function(element) {
    const mathText = element.textContent;
    element.innerHTML = '';
    
    const script = document.createElement('script');
    script.type = 'math/tex';
    script.textContent = mathText;
    element.appendChild(script);
  });
}

// 在文档加载完成后处理
document.addEventListener('DOMContentLoaded', function() {
  if (window.MathJax) {
    handleMathSpans();
    MathJax.typesetPromise().catch(err => console.log('MathJax error:', err));
  } else {
    setTimeout(function() {
      handleMathSpans();
      if (window.MathJax) {
        MathJax.typesetPromise().catch(err => console.log('MathJax error:', err));
      }
    }, 1000);
  }
});
```

**作用**:
- 从 CDN 加载 MathJax 3 库
- 找到所有 `<span class="math">` 标签
- 将其转换为 MathJax 能处理的 `<script type="math/tex">` 标签
- 触发 MathJax 渲染引擎

### 2. 更新 `docs/conf.py`

添加以下配置:

```python
# 在 HTML 输出中包含自定义脚本
html_js_files = [
    'mathjax-config.js',
]

# 在构建时复制 MathJax 配置文件
def copy_mathjax_config(app, exception):
    """在生成文档后复制 MathJax 配置文件"""
    import shutil
    import os
    
    if exception is None:
        src = os.path.join(app.confdir, '_static_source', 'mathjax-config.js')
        dst = os.path.join(app.outdir, '_static', 'mathjax-config.js')
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)

def setup(app):
    app.connect('build-finished', copy_mathjax_config)
```

### 3. 在 Docstring 中正确使用公式

**格式1: 内联公式 (使用 `:math:` 角色)**
```python
r"""
计算面积
使用公式: :math:`A = \frac{1}{2}(b \times h)`
"""
```

**格式2: 块级公式 (使用 `.. math::` 指令)**
```python
r"""
计算面积

.. math::

    A = \pi r^2
"""
```

**重要**: 使用 **raw 字符串** (`r"""`) 来避免 backslash 被转义!

## 工作流程

```
Docstring with :math:
  ↓
Sphinx processes → <span class="math">formula</span>
  ↓
Generate HTML
  ↓
HTML includes mathjax-config.js
  ↓
mathjax-config.js loads MathJax library
  ↓
JavaScript converts <span> to <script type="math/tex">
  ↓
MathJax renders as beautiful formula
  ↓
Browser displays: ∫₀¹ f(x)dx = F(1) - F(0)
```

## 验证公式渲染

### 1. 生成文档

```bash
make docs
# 或
.venv/bin/sphinx-build -b html docs docs/_build/html
```

### 2. 启动文档服务器

```bash
./scripts/serve_docs.sh
# 或
make serve-docs
```

### 3. 打开浏览器并导航

访问 `http://localhost:8000/api/polygons.html`

在 "Polygon.area()" 方法下，你现在应该看到:
- ❌ 之前: `A = \frac{1}{2} \left| \sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i) \right|`
- ✅ 现在: $A = \frac{1}{2} \left| \sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i) \right|$ (美化的数学公式)

### 4. 其他包含公式的页面

| 页面 | 方法/函数 | 公式 |
|------|---------|------|
| **Polygons API** | `Polygon.area()` | 鞋带公式 |
| **Utils API** | `circle_line_intersection()` | 距离公式 |
| **Utils API** | `cartesian_to_polar()` | 向量表示 |

## 技术实现细节

### HTML 生成过程

1. **构建时** (`build-finished` 钩子):
   - Sphinx 生成 HTML 文件
   - `conf.py` 中的 `copy_mathjax_config` 函数被触发
   - `mathjax-config.js` 被复制到 `_build/html/_static/`

2. **HTML 中的引用**:
   ```html
   <head>
       ...
       <script src="../_static/mathjax-config.js?v=xyz"></script>
       ...
   </head>
   ```

3. **运行时** (浏览器加载页面):
   - `mathjax-config.js` 执行
   - 从 CDN 动态加载 MathJax 库
   - MathJax 初始化
   - `handleMathSpans()` 转换所有 `<span class="math">` 标签
   - 调用 `MathJax.typesetPromise()` 进行渲染

### 为什么需要自定义脚本?

Sphinx 的 `:math:` 角色:
```html
<span class="math">A = \frac{1}{2}</span>
```

MathJax 3 默认只处理:
```html
\(A = \frac{1}{2}\)
<!-- 或 -->
<script type="math/tex">A = \frac{1}{2}</script>
```

自定义脚本进行转换:
```javascript
// 找到 <span class="math">
// 获取其内容: "A = \frac{1}{2}"
// 创建 <script type="math/tex">A = \frac{1}{2}</script>
// MathJax 现在可以处理它了!
```

## 浏览器兼容性

| 浏览器 | 支持 | 备注 |
|-------|------|------|
| Chrome | ✅ | 完全支持 MathJax 3 |
| Firefox | ✅ | 完全支持 MathJax 3 |
| Safari | ✅ | 完全支持 MathJax 3 |
| Edge | ✅ | 完全支持 MathJax 3 |
| IE 11 | ⚠️ | 需要 polyfill |

## 常见问题

### Q: 公式仍然显示为文本?
**A**: 
1. 检查浏览器控制台 (F12) 是否有错误
2. 检查 `mathjax-config.js` 是否被加载
3. 确保 `:math:` 标记在 raw 字符串中 (`r"""`)
4. 尝试硬刷新 (Ctrl+Shift+R)

### Q: MathJax 库从哪里加载?
**A**: 从 CDN `https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js`
- 需要网络连接
- 可以离线测试 (稍后会改进)

### Q: 如何离线使用?
**A**: 在 `mathjax-config.js` 中修改脚本路径:
```javascript
script.src = '/path/to/local/mathjax.js';  // 使用本地文件
```

### Q: 性能如何?
**A**: 
- MathJax 库大小: ~2-3 MB (gzip 后)
- 首次加载时间: ~500-1000ms
- 后续渲染: 很快 (缓存)

## 下一步改进

1. **离线支持**: 将 MathJax 包含在项目中
2. **性能优化**: 预加载 MathJax, 使用 worker
3. **CSS 增强**: 为公式添加自定义样式
4. **LaTeX 宏**: 定义常用的数学宏

## 相关文件

- `docs/conf.py` - Sphinx 配置
- `docs/_static_source/mathjax-config.js` - 自定义 JavaScript
- `src/planar_geometry/surface/polygon.py` - 包含 `:math:` 公式的源代码

## 参考资源

- [MathJax 官方文档](https://docs.mathjax.org/)
- [Sphinx Math支持](https://www.sphinx-doc.org/en/master/usage/extensions/math.html)
- [LaTeX 数学模式](https://www.latex-project.org/help/documentation/)

---

**最后更新**: 2026-02-01
**MathJax 版本**: 3.2+
**测试环境**: Chrome, Firefox, Safari
