#!/usr/bin/env bash
# 快速查看Sphinx文档
# 用法: ./scripts/serve_docs.sh

set -e

DOCS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/docs/_build/html"

if [ ! -d "$DOCS_DIR" ]; then
    echo "❌ 文档目录不存在: $DOCS_DIR"
    echo "请先运行: make docs"
    exit 1
fi

echo "📚 启动文档服务器..."
echo "📖 文档位置: $DOCS_DIR"
echo "🌐 访问地址: http://localhost:8000"
echo "⏹️  按 Ctrl+C 停止服务器"
echo ""

cd "$DOCS_DIR"
python3 -m http.server 8000
