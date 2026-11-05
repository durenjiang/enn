#!/usr/bin/env python3
"""游资线 · 共享工具统一入口 (youzi-tool-playbook v1.0.0)

把 9 款共享工具里「本线实测能跑」的动作收成 6 条命令，避免每次重新找路径。
全程只调真实脚本/真实接口，输出即脚本真实输出，不生成、不补写任何数字。

用法:
  python yz.py selftest                       # 行情/双源/抽检 三通道自检
  python yz.py quote 002351                  # 腾讯真实行情（备用通道）
  python yz.py verify 收盘价 11.86 11.86 元   # 双源交叉校验
  python yz.py audit <报告.md>                # 报告落盘前 15% 抽检
  python yz.py guard                         # 8 条否决 + 镜子测试 + 四道闸
  python yz.py routes                        # 9 款工具路由表
"""
import json
import os
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REPORT = r"D:\工作台\游资体系总工作台\工作区-游资\明日行动票预判-20261104-游资.md"


def run(args, timeout=45):
    """调用随技能自带的真实脚本，返回 (rc, 输出文本)。"""
    cmd = [sys.executable, os.path.join(HERE, args[0])] + list(args[1:])
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=timeout)
        out = (p.stdout + p.stderr).decode("utf-8", "replace").strip()
        return p.returncode, out
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT: 脚本超过 %ss 未返回（网络/接口不可用，须在报告写数据缺口）" % timeout
    except Exception as e:
        return 1, "ERROR: %s: %s" % (type(e).__name__, e)


def cmd_quote(code):
    rc, out = run(["ashare_data_win.py", "quote", code])
    print(out)
    return rc


def cmd_verify(field, v1, v2, unit=""):
    values = json.dumps({"源A": v1, "源B": v2}, ensure_ascii=False)
    args = ["financial_rigor.py", "cross-validate", "--field", field,
            "--values", values]
    if unit:
        args += ["--unit", unit]
    rc, out = run(args)
    print(out)
    return rc


def cmd_audit(report):
    if not os.path.isfile(report):
        print("报告不存在：%s" % report)
        return 2
    rc, out = run(["report_audit.py", "extract", "--report", report, "--dry-run"])
    print(out)
    return rc


def cmd_selftest():
    print("=" * 68)
    print("游资线 · 三通道自检（真实脚本 / 真实输出，不编造）")
    print("=" * 68)
    results = []
    # ① 行情（联网，失败记 SKIP 而非伪造）
    rc, out = run(["ashare_data_win.py", "quote", "002351"])
    ok = rc == 0 and ("当前价" in out or "实时行情" in out)
    status = "PASS" if ok else "SKIP"
    results.append(("备用行情(腾讯直连)", status))
    print("\n[1/3] 备用行情 %s" % status)
    print("\n".join("      " + x for x in out.splitlines()[:6]))
    if not ok:
        print("      → 不可用时：改用上一交易日 baostock 收盘，并在报告写「数据缺口」")
    # ② 双源校验（离线，必须 PASS）
    rc, out = run(["financial_rigor.py", "cross-validate", "--field", "自检",
                   "--values", '{"源A":1,"源B":1}', "--unit", ""])
    ok2 = rc == 0 and "数据一致" in out
    results.append(("双源校验", "PASS" if ok2 else "FAIL"))
    print("\n[2/3] 双源校验 %s" % ("PASS" if ok2 else "FAIL"))
    print("\n".join("      " + x for x in out.splitlines()[-4:]))
    # ③ 抽检（依赖报告存在；不存在记 SKIP）
    if os.path.isfile(DEFAULT_REPORT):
        rc, out = run(["report_audit.py", "extract", "--report", DEFAULT_REPORT, "--dry-run"])
        ok3 = rc == 0 and "抽检清单" in out
        results.append(("报告15%抽检", "PASS" if ok3 else "FAIL"))
        print("\n[3/3] 报告抽检 %s" % ("PASS" if ok3 else "FAIL"))
        print("\n".join("      " + x for x in out.splitlines()[:6]))
    else:
        results.append(("报告15%抽检", "SKIP"))
        print("\n[3/3] 报告抽检 SKIP（默认样本不存在，请自行 yz.py audit <报告.md>）")
    print("\n" + "-" * 68)
    print("汇总：" + " | ".join("%s=%s" % (k, v) for k, v in results))
    print("FAIL 必须停下修；SKIP 必须在当日报告写明数据缺口，不得静默降级。")
    print("-" * 68)
    return 0 if all(v != "FAIL" for _, v in results) else 1


GUARD = """
【游资线改写版 · 8 条快速否决清单】（改编自 ai-berkshire/investment-checklist，非上游原文）
触发任意一条 → 直接「否决」，出观望信号并逐条写明拦截原因：
  [ ] 1. 说不清这票为什么涨 / 赚钱逻辑讲不清
  [ ] 2. 公告或财务红项未排除（立案、ST、减持、业绩雷、解禁）
  [ ] 3. 管理层诚信污点 / 监管问询未澄清
  [ ] 4. 主线退潮、板块转弱、情绪档位不支持（退潮=0仓）
  [ ] 5. 靠「下一个接盘者出更高价」赚钱（高位连板 / 博傻）
  [ ] 6. 单笔亏损超出 ≤2% 铁闸、无 7% 止损兜底
  [ ] 7. 买入理由主要是「别人都在买」或「最近涨得好」→ 禁追高
  [ ] 8. 200 字写不清买入理由
【镜子测试】5 句话说不完整 = 不买，没有例外。
【三态结论】通过 / 不通过 / 灰色地带（数据不足就留白，禁止硬填、禁止编造）。
【四道闸】①真实取数 → ②双源校验 → ③15%抽检 → ④本清单 → 落盘 + 任务完成标记。
【红线】只做多 / 不加杠杆 / A1–A7 / 风控铁闸 / VETO 未解除只观察档不打 / 龙虎榜 T+1 / 标【模拟】 / 不构成投资建议。
"""

ROUTES = """
【9 款共享工具路由】（权威版：A股量化工具集/机器人调用指引.md）
  a-stock-data              查接口/备选数据源（零依赖，直读）
  sequoia-x                 7 策略候选池（只当候选，不当信号）
  stock-picker-plus         三维评分交叉
  a-stock-short-term-backtest 28 策略共振（重跑前必改 END 为当日）
  daily_stock_analysis      缺 LLM Key 不启用；只借引擎名当字段模板
  tickflow-stock-panel      5% 动手线 / 真实成本（往返≈0.19%，保守0.30%）
  UZI-Skill                 排雷 trap-detector / 龙虎榜 lhb-analyzer（T+1）
  PanWatch                  观察票提醒规则 / 机会页 7 字段（含失效条件）
  ai-berkshire              双源校验 / 15%抽检 / 备用行情 / 8 条否决（非信号源）
  —— 本线脚本 ——
  yz.py quote / verify / audit / guard / selftest / routes（本技能自带）
  screen_baostock.py        原型① 横盘突破筛选（baostock 真实日线）
"""


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    c = a[0]
    if c == "quote":
        if len(a) < 2:
            print("用法: yz.py quote <6位代码>")
            return 2
        return cmd_quote(a[1])
    if c == "verify":
        if len(a) < 4:
            print("用法: yz.py verify <字段> <源A值> <源B值> [单位]")
            return 2
        return cmd_verify(a[1], a[2], a[3], a[4] if len(a) > 4 else "")
    if c == "audit":
        if len(a) < 2:
            print("用法: yz.py audit <报告.md>")
            return 2
        return cmd_audit(a[1])
    if c == "selftest":
        return cmd_selftest()
    if c == "guard":
        print(GUARD)
        return 0
    if c == "routes":
        print(ROUTES)
        return 0
    print("未知命令: %s（可用: selftest / quote / verify / audit / guard / routes）" % c)
    return 2


if __name__ == "__main__":
    sys.exit(main())
