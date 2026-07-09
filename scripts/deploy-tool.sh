#!/usr/bin/env bash
set -euo pipefail

# deploy-tool.sh — 一键部署工具到仪表盘
# 用法: ./scripts/deploy-tool.sh <工具slug> <图标> <标题> <描述> <颜色> <源HTML文件>
# 示例: ./scripts/deploy-tool.sh my-tool 🔧 "我的工具" "描述文字" "#1a2a3a" ./my-tool.html

if [ $# -ne 6 ]; then
  echo "用法: $0 <slug> <icon> <title> <desc> <color> <html-file>"
  echo "示例: $0 my-tool 🔧 '我的工具' '描述' '#1a2a3a' ./my-tool.html"
  exit 1
fi

SLUG="$1"
ICON="$2"
TITLE="$3"
DESC="$4"
COLOR="$5"
HTML_FILE="$6"

PROJ_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TOOLS_JSON="$PROJ_DIR/user_output/tools.json"
TARGET_DIR="$PROJ_DIR/user_output/$SLUG"
TARGET_FILE="$TARGET_DIR/index.html"

# 检查源文件
if [ ! -f "$HTML_FILE" ]; then
  echo "错误: 源文件不存在: $HTML_FILE"
  exit 1
fi

# 创建目录并复制
mkdir -p "$TARGET_DIR"
cp "$HTML_FILE" "$TARGET_FILE"
echo "✓ 已复制到 $TARGET_FILE"

# 添加到 tools.json（在第一个 ] 前插入新条目）
if grep -q '"type":' "$TOOLS_JSON" 2>/dev/null; then
  # 有现有条目，在最后一条后加逗号和新条目
  sed -i 's/\(.*\)\]$/  \1,/' "$TOOLS_JSON" 2>/dev/null || true
  # 直接用 Python 或更可靠的方式添加
  python3 -c "
import json, sys
path = '$TOOLS_JSON'
with open(path) as f:
    tools = json.load(f)
tools.append({
    'icon': '$ICON',
    'name': '$TITLE',
    'desc': '$DESC',
    'href': '/$SLUG',
    'color': '$COLOR',
    'type': 'static'
})
with open(path, 'w') as f:
    json.dump(tools, f, ensure_ascii=False, indent=2)
    f.write('\n')
"
  echo "✓ 已添加到 tools.json"
else
  # 工具 JSON 还不存在，创建它
  cat > "$TOOLS_JSON" <<EOF
[
  {"icon":"$ICON","name":"$TITLE","desc":"$DESC","href":"/$SLUG","color":"$COLOR","type":"static"}
]
EOF
  echo "✓ 已创建 tools.json"
fi

# git 自动追踪
cd "$PROJ_DIR"
git add "$TARGET_FILE" "$TOOLS_JSON" 2>/dev/null || true

echo ""
echo "✅ 部署完成！还需手动完成以下步骤："
echo ""
echo "  1. 添加 nginx 路由（新工具首次部署需要）："
echo "     location /$SLUG/ {"
echo "         root /iptv-api/user_output;"
echo "     }"
echo ""
echo "  2. 同步容器："
echo "     docker cp $PROJ_DIR/user_output iptv-api:/iptv-api/user_output"
echo "     docker exec iptv-api nginx -s reload"
echo ""
echo "  3. 提交代码："
echo "     git commit -m \"添加 $TITLE\""
echo "     git push"
