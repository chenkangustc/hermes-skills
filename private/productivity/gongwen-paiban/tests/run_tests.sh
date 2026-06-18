#!/usr/bin/env bash
#
# gongwen-paiban 回归测试运行器
# 用法: ./run_tests.sh [--quiet]
#
# 每次更新 skill 后，运行此脚本验证：
# 1. 字体可用性
# 2. PDF 正确生成
# 3. python-docx 正确生成（如已安装）
# 4. SKILL.md 规范性

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON="/usr/bin/python3"

PASS=0
FAIL=0

header() {
    echo ""
    echo "========================================"
    echo "  $1"
    echo "========================================"
}

run_test() {
    local name="$1"
    local script="$2"
    echo ""
    echo "--- $name ---"
    if "$PYTHON" "$script"; then
        echo "  ✅ PASS: $name"
        ((PASS++))
    else
        echo "  ❌ FAIL: $name"
        ((FAIL++))
    fi
}

echo "============================================"
echo "  公文排版技能 (gongwen-paiban) 回归测试"
echo "  技能路径: $SKILL_DIR"
echo "  运行时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================"

# ── 1. 字体可用性 ──────────────────────────────
header "字体可用性测试"
run_test "字体检查" "$SCRIPT_DIR/test_fonts.py"

# ── 2. PDF 生成 ────────────────────────────────
header "PDF 生成测试"
run_test "PDF 生成" "$SCRIPT_DIR/test_gongwen_pdf.py"

# ── 3. python-docx ─────────────────────────────
header "python-docx 测试"
run_test "docx 生成" "$SCRIPT_DIR/test_gongwen_docx.py"

# ── 4. 规范性测试 ───────────────────────────────
header "规范性测试"
run_test "SKILL 规范" "$SCRIPT_DIR/test_gongwen_validity.py"

# ── 汇总 ──────────────────────────────────────
echo ""
echo "============================================"
echo "  测试汇总"
echo "============================================"
echo "  ✅ 通过: $PASS"
echo "  ❌ 失败: $FAIL"
echo ""

if [ "$FAIL" -eq 0 ]; then
    echo "  🎉 全部测试通过！"
    exit 0
else
    echo "  ⚠️  有 $FAIL 个测试失败，请检查后更新技能。"
    exit 1
fi
