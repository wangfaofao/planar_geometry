#!/usr/bin/env bash
# 快速查看Sphinx文档
# 用法: 
#   ./scripts/serve_docs.sh              # 使用默认端口 8000
#   ./scripts/serve_docs.sh 8080         # 使用指定端口 8080
#
# 环境要求:
#   - 虚拟环境: .venv/ (使用 uv 或 venv 创建)
#   - 文档已生成: docs/_build/html/
#
# 如果文档还未生成，使用:
#   make docs       # 使用 Makefile
#   或
#   .venv/bin/sphinx-build -b html docs docs/_build/html

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DOCS_DIR="$PROJECT_ROOT/docs/_build/html"
VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python"

# 检查虚拟环境中的Python
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ 虚拟环境Python不存在: $VENV_PYTHON"
    echo ""
    echo "请先创建虚拟环境："
    echo "  uv venv                          # 使用 uv"
    echo "  或"
    echo "  python -m venv .venv             # 使用 venv"
    echo "  source .venv/bin/activate        # 激活"
    exit 1
fi

if [ ! -d "$DOCS_DIR" ]; then
    echo "❌ 文档目录不存在: $DOCS_DIR"
    echo ""
    echo "请先生成文档："
    echo "  make docs"
    echo "  或"
    echo "  .venv/bin/sphinx-build -b html docs docs/_build/html"
    exit 1
fi

PORT="${1:-8000}"

# 检查端口是否被占用
if command -v lsof &> /dev/null; then
    if lsof -i :$PORT &> /dev/null; then
        echo "⚠️  端口 $PORT 已被占用"
        echo "请尝试使用另一个端口: ./scripts/serve_docs.sh 8001"
        exit 1
    fi
fi

echo ""
echo "📚 启动文档服务器..."
echo "📖 文档位置: $DOCS_DIR"
echo "🌐 访问地址: http://localhost:$PORT"
echo "⏹️  按 Ctrl+C 停止服务器"
echo ""

cd "$DOCS_DIR"
"$VENV_PYTHON" -m http.server "$PORT"

