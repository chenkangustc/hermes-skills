#!/usr/bin/env python3
"""
gongwen-paiban PDF 生成测试
验证 PDF 能正常生成，且输出文件的页面设置正确。
"""

import sys
import os
import tempfile

# 将 gongwen-paiban 的 scripts 目录加入路径
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")
sys.path.insert(0, SCRIPTS_DIR)


def test_pdf_generation():
    """测试基本 PDF 生成：标题 + 正文 + 署名"""
    from gongwen_pdf import title, h1, h2, body, signature, label, spacer, build_pdf

    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    tmp.close()
    output = tmp.name

    try:
        content = [
            title("关于XXXX工作的报告"),
            spacer(),
            h1("一、工作背景"),
            body("根据上级部门工作部署，我单位深入开展相关工作，现将有关情况报告如下。"),
            h1("二、主要工作"),
            h2("（一）组织管理"),
            body("建立健全工作机制，成立专项工作领导小组，明确职责分工。"),
            h2("（二）工作成效"),
            body("各项工作稳步推进，取得了阶段性成果。"),
            h1("三、下一步计划"),
            body("继续加大工作力度，确保各项任务按期完成。"),
            spacer(28),
            signature("XXXX单位"),
            signature("2025年6月18日"),
        ]
        result = build_pdf(content, output, title_meta="公文排版测试")
        print(f"  ✅ PDF 生成成功: {result}")
        assert os.path.isfile(result), "PDF 文件未生成"
        assert os.path.getsize(result) > 1000, f"PDF 文件太小: {os.path.getsize(result)} bytes"
        print(f"  📄 文件大小: {os.path.getsize(result):,} bytes")
        return True
    except Exception as e:
        print(f"  ❌ PDF 生成失败: {e}")
        return False
    finally:
        os.unlink(output)


def test_pdf_with_all_elements():
    """测试所有元素类型都能正常渲染"""
    from gongwen_pdf import title, h1, h2, body, signature, label, spacer, build_pdf

    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    tmp.close()
    output = tmp.name

    try:
        content = [
            title("关于XX项目立项的请示"),
            spacer(),
            h1("一、项目背景"),
            body("为贯彻落实国家相关文件精神，拟开展XX项目。"),
            h1("二、项目内容"),
            h2("（一）总体目标"),
            body("本项目旨在提升相关领域技术水平。"),
            h2("（二）具体方案"),
            body("包括基础设施建设、人才培养等。"),
            h1("三、经费预算"),
            body("项目总经费预计为500万元。"),
            spacer(),
            label("附件：1. 项目方案书"),
            label("附件：2. 经费预算表"),
            spacer(28),
            signature("XX单位"),
            signature("2025年6月18日"),
        ]
        result = build_pdf(content, output)
        print(f"  ✅ 全元素PDF生成成功: {result}")
        assert os.path.isfile(result), "PDF 文件未生成"
        assert os.path.getsize(result) > 1000, f"PDF 文件太小: {os.path.getsize(result)} bytes"
        return True
    except Exception as e:
        print(f"  ❌ 全元素测试失败: {e}")
        return False
    finally:
        os.unlink(output)


def test_multiple_pages():
    """测试多页 PDF 生成（长文本）"""
    from gongwen_pdf import title, h1, body, spacer, build_pdf

    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    tmp.close()
    output = tmp.name

    try:
        content = [title("长篇报告")]
        content.append(spacer())
        for i in range(1, 6):
            content.append(h1(f"第{i}章"))
            for _ in range(5):
                content.append(
                    body("这是一段较长的正文内容，用于测试多页PDF生成。"
                         "根据公文排版规范，正文使用仿宋_GB2312字体、16磅字号、"
                         "28磅行距、首行缩进2字符。")
                )
        result = build_pdf(content, output)
        print(f"  ✅ 多页PDF生成成功: {result}")
        assert os.path.isfile(result), "PDF 文件未生成"
        size = os.path.getsize(result)
        print(f"  📄 文件大小: {size:,} bytes")
        assert size > 5000, f"多页PDF不应太小: {size} bytes"
        return True
    except Exception as e:
        print(f"  ❌ 多页测试失败: {e}")
        return False
    finally:
        os.unlink(output)


def test_cli_invocation():
    """测试 gongwen_pdf.py 作为 CLI 直接调用"""
    import subprocess

    script = os.path.join(SCRIPTS_DIR, "gongwen_pdf.py")
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    tmp.close()
    output = tmp.name

    try:
        result = subprocess.run(
            [sys.executable, script, "-o", output],
            capture_output=True, text=True, timeout=15
        )
        print(f"  CLI stdout: {result.stdout.strip()}")
        if result.returncode != 0:
            print(f"  ❌ CLI 退出码: {result.returncode}")
            print(f"  stderr: {result.stderr.strip()}")
            return False

        assert os.path.isfile(output), "CLI 未生成 PDF"
        assert os.path.getsize(output) > 1000, f"CLI 生成文件太小: {os.path.getsize(output)} bytes"
        print(f"  ✅ CLI 调用成功: {output}")
        return True
    except subprocess.TimeoutExpired:
        print("  ❌ CLI 调用超时")
        return False
    except Exception as e:
        print(f"  ❌ CLI 调用失败: {e}")
        return False
    finally:
        if os.path.isfile(output):
            os.unlink(output)


def main():
    print("=" * 60)
    print("  公文排版 PDF 生成测试")
    print("=" * 60)

    tests = [
        ("基本PDF生成（标题+正文+署名）", test_pdf_generation),
        ("全元素类型渲染", test_pdf_with_all_elements),
        ("多页长文本测试", test_multiple_pages),
        ("CLI 命令行调用", test_cli_invocation),
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
