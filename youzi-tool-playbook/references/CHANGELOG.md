# CHANGELOG · youzi-tool-playbook

## v1.0.0 · 2026-11-05（首发 · 游资线专属）

- **新建**，不修改任何既有技能（`ashare-toolset-collab` / `ashare-quant-toolkit` 属友军域，保持只读）。
- 覆盖共享技能库 **9 款工具**（原 6 款 + UZI-Skill + PanWatch + ai-berkshire），把「怎么用 / 如何用好」内化为：① 加载后第一动作 → ② 决策树 → ③ 四道质检闸 → ④ 一键命令 → ⑤ 失败回退 → ⑥ 铁律与域边界 → ⑦ 自我进化。
- 新增可执行入口 `scripts/yz.py`：`selftest / quote / verify / audit / guard / routes`；随包带 3 个实测脚本（`ashare_data_win.py` 游资线 Windows 适配、`financial_rigor.py`、`report_audit.py`，后两者上游 MIT 零依赖）。
- 新增 `references/9工具速查.md`（入口/状态/禁用/数据源回退链）与 `references/落盘质检清单.md`（四道闸逐项 + K-07 模板2 七段映射 + 回执死命令）。
- **本机实测**：`yz.py selftest` 3/3 PASS（腾讯备用行情 002351 收 12.27 / +3.46%；双源校验偏差 0%；11-04 战报抽检 12 点抽 3 点）。
- 落点：用户级技能 `~/.workbuddy/skills/youzi-tool-playbook/`（可被 Skill 直接加载）、共享工具区-游资/技能包、共享技能库、enn 仓库。
- 红线：不是买卖信号源；VETO 未解除只出观察档不打；作者口径数字禁进战报；禁编造；标【模拟】、不构成投资建议。

## 待办 / 已知边界（不隐瞒）

- 22 个 AI Berkshire Skill 的完整 Claude Code/Codex 多 Agent 流程**未实跑**；本技能只用 md 模板 + 零依赖 py。
- PanWatch / UZI-Skill 服务栈与 Python 依赖**未实跑**，只做静态复用。
- `daily_stock_analysis` 缺 LLM Key 不启用；`a-stock-short-term-backtest` 的 `END` 为复发型硬编码，重跑前必改。
- 未来若共享库新增第 10 款：更新本技能 §2 决策树、§5 速查表、`references/9工具速查.md`，并升版本号（不覆盖 v1.0.0）。
