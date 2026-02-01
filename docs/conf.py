# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from datetime import datetime

# Add source directory to path
sys.path.insert(0, os.path.abspath("../src"))

# -- Project information -----------------------------------------------
project = "planar_geometry"
copyright = f"{datetime.now().year}, wangheng"
author = "wangheng"
release = "0.2.0"
version = "0.2"

# -- General configuration -------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "**.ipynb_checkpoints"]
language = "en"

# -- Napoleon extension settings ------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_method = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# -- Autodoc settings ------------------------------------------------------
autodoc_typehints = "description"
autodoc_typehints_format = "short"
autodoc_member_order = "bysource"
autoclass_content = "both"

# -- Math rendering settings ------------------------------------------------
# 使用 MathJax 3 渲染 LaTeX 公式
mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"

# 在 HTML 输出中包含自定义脚本来处理 .math 标签
html_js_files = []


# 在构建时复制自定义的 mathjax-config.js 文件
def copy_mathjax_config(app, exception):
    """在生成文档后复制 MathJax 配置文件"""
    import shutil
    import os

    if exception is None:  # 只在成功生成时复制
        src = os.path.join(app.confdir, "_static_source", "mathjax-config.js")
        dst = os.path.join(app.outdir, "_static", "mathjax-config.js")
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)


def setup(app):
    app.connect("build-finished", copy_mathjax_config)


# -- HTML output -------------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_theme_options = {}
html_static_path = ["_static"]
html_logo = None
html_favicon = None
html_last_updated_fmt = "%Y-%m-%d"

# -- Intersphinx mapping ------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
}

# -- Options for LaTeX output ------------------------------------
latex_elements = {
    "papersize": "letterpaper",
    "pointsize": "12pt",
    "preamble": r"""
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{textcomp}
\usepackage{amssymb}
\DeclareUnicodeCharacter{00A0}{\nobreakspace}
""",
    "figure_align": "htbp",
    "fncychap": "",
}
latex_documents = [
    ("index", "planar_geometry.tex", "planar_geometry Documentation", "Contributors", "manual"),
]

# -- Options for EPUB output ----------------------------------------
epub_basename = "planar_geometry"
