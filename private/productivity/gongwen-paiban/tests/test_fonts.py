#!/usr/bin/env python3
"""
gongwen-paiban 字体可用性测试
验证所有公文字体已正确安装且可注册。
"""

import sys
import os


def check_font_installed(font_name: str, font_path: str) -> bool:
    """检查字体文件是否存在（fc-list 结果仅供参考，TTC 字体可能不显示为独立族名）"""
    if not os.path.isfile(font_path):
        print(f"  ❌ 文件不存在: {font_path}")
        return False

    # 文件存在就算通过（TTC 字体 fc-list 不一定会列出每个子族名）
    print(f"  ✅ 文件存在: {font_path} ({os.path.getsize(font_path):,} bytes)")
    return True


def check_reportlab_register(font_path: str, font_alias: str) -> bool:
    """测试 reportlab 能否注册该字体"""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    try:
        pdfmetrics.registerFont(TTFont(font_alias, font_path))
        print(f"  ✅ reportlab 注册成功: {font_alias}")
        return True
    except Exception as e:
        print(f"  ❌ reportlab 注册失败 [{font_alias}]: {e}")
        return False


def main():
    print("=" * 60)
    print("  公文排版字体测试")
    print("=" * 60)

    fonts = {
        "方正小标宋简体": "/usr/share/fonts/truetype/gongwen/方正小标宋体.TTF",
        "仿宋_GB2312": "/usr/share/fonts/truetype/gongwen/SIMFANG_0.TTF",
        "楷体_GB2312": "/usr/share/fonts/truetype/gongwen/SIMKAI_0.TTF",
        "黑体(文泉驿正黑)": "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "Times New Roman": "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf",
    }

    all_ok = True

    print("\n[1/2] 字体文件检查")
    print("-" * 40)
    for name, path in fonts.items():
        if not check_font_installed(name, path):
            all_ok = False

    print("\n[2/2] reportlab 注册测试")
    print("-" * 40)
    for name, path in fonts.items():
        alias = {
            "方正小标宋简体": "FZXiaoBiaoSong",
            "仿宋_GB2312": "FangSong_GB2312",
            "楷体_GB2312": "KaiTi_GB2312",
            "黑体(文泉驿正黑)": "HeiTi",
            "Times New Roman": "TimesNewRoman",
        }[name]
        if not check_reportlab_register(path, alias):
            all_ok = False

    print("\n" + "=" * 60)
    if all_ok:
        print("  ✅ 全部字体测试通过")
        return 0
    else:
        print("  ❌ 部分字体测试未通过，请检查上方详情")
        return 1


if __name__ == "__main__":
    ret = main()
    print(f"\n测试结果: {'✅ 通过' if ret == 0 else '❌ 失败'} (exit={ret})")
    sys.exit(ret)
