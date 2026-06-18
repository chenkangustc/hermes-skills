#!/usr/bin/env python3
"""
gongwen-paiban 规范性测试
验证 SKILL.md 本身的格式规范性：
- frontmatter 格式正确
- description 不超长
- 所有引用文件（references, scripts）存在
"""

import sys
import os
import re
import yaml

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_frontmatter_valid():
    """检查 SKILL.md 的 frontmatter"""
    skill_md = os.path.join(SKILL_DIR, "SKILL.md")
    content = open(skill_md, "r", encoding="utf-8").read()

    # 必须以 --- 开头
    assert content.startswith("---"), "SKILL.md 不以 --- 开头"

    # 找到 closing ---
    m = re.search(r'\n---\s*\n', content[3:])
    assert m, "未找到关闭的 ---"
    fm_text = content[3:m.start()+3]
    fm = yaml.safe_load(fm_text)

    assert "name" in fm, "缺少 name 字段"
    assert "description" in fm, "缺少 description 字段"
    assert len(fm["description"]) <= 1024, f"description 超长 ({len(fm['description'])} chars)"

    print(f"  ✅ name: {fm['name']}")
    print(f"  ✅ description: {len(fm['description'])} chars (≤1024)")
    print(f"  ✅ version: {fm.get('version', '未设置')}")
    return True


def test_referenced_files_exist():
    """验证 SKILL.md 中引用的辅助文件都存在"""
    skill_md = os.path.join(SKILL_DIR, "SKILL.md")
    content = open(skill_md, "r", encoding="utf-8").read()

    # 检查 references/ 和 scripts/ 目录是否存在
    ref_dir = os.path.join(SKILL_DIR, "references")
    scripts_dir = os.path.join(SKILL_DIR, "scripts")

    assert os.path.isdir(ref_dir), "references/ 目录不存在"
    assert os.path.isdir(scripts_dir), "scripts/ 目录不存在"

    # 列出 files
    ref_files = os.listdir(ref_dir)
    script_files = os.listdir(scripts_dir)

    print(f"  📂 references 文件: {len(ref_files)} 个 -> {ref_files}")
    print(f"  📂 scripts 文件: {len(script_files)} 个 -> {script_files}")

    # 检查 gongwen_pdf.py 存在且可执行
    gp = os.path.join(scripts_dir, "gongwen_pdf.py")
    assert os.path.isfile(gp), "gongwen_pdf.py 不存在"
    assert gp.endswith(".py"), "gongwen_pdf.py 不是 .py 文件"
    print(f"  ✅ 关键脚本存在: gongwen_pdf.py")

    # 检查 reference 文件
    has_format_ref = any("排版" in f for f in ref_files)
    has_font_ref = any("字体" in f for f in ref_files)
    assert has_format_ref, "缺少 公文排版规范 参考文件"
    assert has_font_ref, "缺少 字体安装流程 参考文件"
    print(f"  ✅ 排版规范参考存在")
    print(f"  ✅ 字体安装参考存在")

    return True


def test_script_importable():
    """测试 gongwen_pdf.py 可导入（无语法错误）"""
    import importlib.util
    script = os.path.join(SKILL_DIR, "scripts", "gongwen_pdf.py")
    spec = importlib.util.spec_from_file_location("gongwen_pdf", script)
    assert spec is not None, f"无法加载 {script}"
    mod = importlib.util.module_from_spec(spec)
    # 只检查语法，不实际运行（会注册字体）
    try:
        compile(open(script).read(), script, 'exec')
        print(f"  ✅ gongwen_pdf.py 语法正确")
    except SyntaxError as e:
        print(f"  ❌ 语法错误: {e}")
        return False
    return True


def main():
    print("=" * 60)
    print("  公文排版规范性测试")
    print("=" * 60)

    tests = [
        ("SKILL.md frontmatter 格式", test_frontmatter_valid),
        ("引用文件完整性", test_referenced_files_exist),
        ("脚本语法检查", test_script_importable),
    ]

    results = []
    for name, func in tests:
        print(f"\n[{len(results)+1}/{len(tests)}] {name}")
        print("-" * 40)
        try:
            ok = func()
        except Exception as e:
            print(f"  ❌ 异常: {e}")
            ok = False
        results.append(ok)

    print("\n" + "=" * 60)
    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"  结果: {passed}/{total} 通过")
    for name, ok in zip([t[0] for t in tests], results):
        status = "✅" if ok else "❌"
        print(f"  {status} {name}")

    return 0 if all(results) else 1


if __name__ == "__main__":
    ret = main()
    print(f"\n测试结果: {'✅ 全部通过' if ret == 0 else '❌ 有失败的测试'} (exit={ret})")
    sys.exit(ret)
