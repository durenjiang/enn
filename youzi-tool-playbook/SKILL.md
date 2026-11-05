---
name: youzi-tool-playbook
description: >-
  游资线专属技能：把军团共享技能库 9 款 A股工具（a-stock-data / sequoia-x / stock-picker-plus / a-stock-short-term-backtest / daily_stock_analysis / tickflow-stock-panel / UZI-Skill / PanWatch / ai-berkshire）编成本线可执行的作战流程——盘前备用行情取数、原型①选票、排雷、双源校验、报告落盘前 15% 抽检、8 条否决清单、5% 动手线复核、任务完成标记。凡游资线涉及【工具怎么用 / 选票预判 / 战报落盘 / 数据校验 / 盘前定调 / 午后复核 / 收盘复盘 / 夜间巡检 / 共享库取用】的任务自动加载。触发词：游资工具、共享技能库、9款工具、明日行动票预判、原型①、盘前定调、落盘质检、双源校验、报告抽检、腾讯行情备用通道、ashare_data_win、AI Berkshire、UZI-Skill、PanWatch、tickflow 5%、任务完成标记、游资线怎么用工具。
version: 1.0.0
agent_created: true
display_name: "游资线·共享工具作战技能"
display_name_en: "Youzi Shared Toolkit Playbook"
description_zh: "游资线专属：9 款共享工具怎么用、如何用好、如何内化成本线流程（含一键可执行自检）。"
description_en: "Youzi-line playbook for the 9 shared A-share tools, with executable quality gates."
visibility: "public"
---

# 游资线 · 共享工具作战技能（v1.0.0 / 2026-11-05）

> 这不是第 10 款工具，是**把 9 款工具变成游资线自己的动作**：什么时候用哪个、跑完怎么验、验完怎么落盘。
> 全部【模拟】、不构成投资建议；**VETO 未解除 → 全批观察档、不打**。

## 0. 与其他技能的分工（不重复、不改别人文件）

| 技能 | 归属 | 管什么 |
|---|---|---|
| `ashare-toolset-collab` | ETF/量化线维护 | 6 工具时代的**跨机器人协作协议**、域边界、飞书推送、平行基金复核 |
| `ashare-quant-toolkit` | 个人量化（军师） | 6 工具在 11-07 最终评定中的达标线、END 坑 SOP、八原型编排 |
| **本技能** | **游资线自己** | **9 款工具在游资线日常四档任务中的取数与质检动作**；新增 UZI-Skill / PanWatch / ai-berkshire 的用法与实测坑 |

冲突时：**铁律与数据真实性以本技能为准（更严）**；协作边界与推送仍遵 `ashare-toolset-collab`；**绝不修改上述两技能或任何友军域文件**。

## 1. 加载后第一动作（每次必做，顺序不能换）

1. **先读最新指令**：`D:\工作台\游资体系总工作台\工作区-游资\` 下按修改时间取最新的 `数据通道升级令*`/`催办单*`/`审核意见*`/`派单*`，按最新指令干活。
2. **确认环境档位与 VETO**：退潮=0仓；VETO 未解除只出观察档。
3. **跑 `python scripts/yz.py selftest`**：确认行情/校验/抽检三条通道今天是否活着；**任一失败就写进报告的「数据缺口」，不编造、不静默降级**。
4. 再按 §2 决策树选工具。

## 2. 决策树 ·「我要…→ 用哪个」

| 我要 | 用 | 命令 / 入口 | 产出必须带 |
|---|---|---|---|
| 盘前取真实行情（akshare 空快照时） | `ashare_data_win.py`（腾讯直连） | `python scripts/yz.py quote 002351` | 数据时间戳 + 换手率/流通市值 |
| 取日线、换手率做原型①筛选 | baostock（本线 `screen_baostock.py`） | `query_history_k_data_plus` 带 `turn` | 平台高点/量比/vwap20 主力成本 |
| 出《明日行动票预判》 | 原型①口径 + DSA 策略 id 做选票逻辑模板 | 横盘≥40日 + 量≥2×5日均 + 收≥平台高点 + 换手≥3% + 成交额≥3亿 | 每票【逻辑/方向/可信度/主力成本】 |
| 给入选票排雷 / 看游资席位 | `UZI-Skill` → `trap-detector` / `lhb-analyzer` | 读 `UZI-Skill/SKILL.md` 后分发 | 证据 + 龙虎榜 T+1 标注 |
| 观察票触发提醒 / 执行纪律 | `PanWatch` 提醒规则 + 机会页 7 字段 | 读 `PanWatch/README.zh-CN.md` | 失效条件 / 止损 / 归因 |
| 验证 5% 动手线 / 真实成本 | `tickflow-stock-panel` 成本模型 | `fees_pct=0.0002` + `slippage_bps=5`（往返≈0.19%，保守 0.30%） | 胜率 + 均净 + 成本口径 |
| 核对两个通道的数字是否一致 | `financial_rigor.py` | `python scripts/yz.py verify 收盘价 11.86 11.86 元` | 偏差% 与共识值 |
| 战报落盘前复核数字 | `report_audit.py` | `python scripts/yz.py audit <报告.md>` | 抽检清单 + 准出/打回 |
| 防止追高 / 强制给结论 | 8 条否决清单 + 镜子测试（游资改写版） | `python scripts/yz.py guard` | 通过 / 不通过 / 灰色地带 |
| 查数据接口 / 备选数据源 | `a-stock-data` 接口字典（零依赖，直读） | 共享库 `a-stock-data_接口清单_SKILL.md` | 来源标注 |
| 批量候选 / 因子评分 / 回测 | sequoia-x / stock-picker-plus / a-stock-short-term-backtest | 见 `references/9工具速查.md` | ⚠️ 只当候选池，不当信号源 |
| 不知道该用哪个 | 路由表 | `python scripts/yz.py routes` | — |

> **三不**：不把任何工具的输出当买卖信号；不把作者口径（Star / 命中数 / 自报收益）当本线数据；不跳过 §3 四道闸。

## 3. 如何用好 · 四道质检闸（本技能的核心，缺一不落盘）

```
① 真实取数  → ② 双源校验  → ③ 15% 抽检  → ④ 8条否决 + 镜子测试  → 落盘 + 任务完成标记
```

| 闸 | 动作 | 不通过怎么办 |
|---|---|---|
| ① 真实 | 只用真实接口实拉；盘前 09:00–09:30 akshare 空值 → 改腾讯直连或上一交易日 baostock 收盘 | 写「数据缺口」，**不得编造任何数字** |
| ② 双源 | 关键数字（收盘价 / vwap20 成本 / 突破缺口）两个独立来源交叉，偏差 >2% 标红 | 标「口径不一致」，报告里逐条写明，不硬填 |
| ③ 抽检 | 落盘前对待发报告跑 `audit`，抽 15% 数据点复核 | 打回重取；抽检信源换成 baostock/新浪/腾讯（上游默认东财+巨潮偏财务口径，套短线价格会错配） |
| ④ 否决 | `guard` 输出三态结论；5 句话说不清买入逻辑＝不买；数据不足＝**灰色地带**而非硬填 | 直接出观望，逐条说明拦截原因 |

**落盘固定动作**：产出写回 `工作区-游资\` → 写《任务完成标记-YYYYMMDD-游资.md》（指令完成情况 / 产出路径 / 诚实上报的缺口）→ 报告末尾附**引用的本地文档清单** → 标【模拟】+ 不构成投资建议。

## 4. 一键命令（脚本随技能自带，已本机实测）

```bash
SK=~/.workbuddy/skills/youzi-tool-playbook/scripts
python $SK/yz.py selftest                  # 三条通道自检（行情/双源/抽检），输出 PASS/SKIP/FAIL
python $SK/yz.py quote 002351              # 腾讯真实行情（换手/流通市值/PE/PB）
python $SK/yz.py verify 收盘价 11.86 11.86 元   # 双源校验
python $SK/yz.py audit <报告.md>           # 15% 抽检（dry-run）
python $SK/yz.py guard                     # 8 条否决 + 镜子测试 + 四道闸
python $SK/yz.py routes                    # 9 款工具路由表
```

`scripts/` 内含：`yz.py`（统一入口）、`ashare_data_win.py`（游资线 Windows 适配）、`financial_rigor.py`、`report_audit.py`（后两者为上游零依赖脚本，MIT）。

## 5. 九款速查（能跑 / 只读 / 禁用）

| 工具 | 本线状态 | 用在哪 |
|---|---|---|
| a-stock-data | ✅ 零依赖直读 | 查接口、备选数据源 |
| sequoia-x | ⚠️ 已收录、只作候选池 | 7 策略口径参照；作者「无一超额为正」 |
| stock-picker-plus | ⚠️ 已收录 | 三维评分交叉 |
| a-stock-short-term-backtest | ⚠️ 重跑前必改 `update_data.py` 的 `END` 为当日 | 28 策略共振（个人量化维护，本线只借结论） |
| daily_stock_analysis | ❌ 缺 LLM Key 不启用 | `shrink_pullback` / `volume_breakout` **只当字段模板** |
| tickflow-stock-panel | ✅ 成本模型已核验 | 5% 动手线 / 真实成本压测 |
| UZI-Skill | ✅ 只读静态（未实跑） | 排雷 / 龙虎榜 T+1 / 深研 |
| PanWatch | ✅ 只读静态（服务栈重） | 提醒规则 / 机会页 7 字段 |
| **ai-berkshire** | ✅ **3 脚本本机实跑通过** | 双源校验 / 抽检 / 备用行情 / 8 条否决；**不是信号源** |

完整入口、依赖、坑、禁用项见 `references/9工具速查.md`。

## 6. 实测坑与失败回退（2026-11-05 本机真踩过）

| 现象 | 原因 | 回退 |
|---|---|---|
| 盘前 `akshare.stock_zh_a_spot()` 返回 5577 行全 0 | 预开盘占位数据 | 腾讯 `qt.gtimg.cn` 直连（`--noproxy "*"`）或上一交易日 baostock 收盘 |
| 新浪快照无换手率/量比/总市值列 | 东财专有列 | baostock `turn` 字段 / 腾讯行情 |
| 东财系接口断连限流 | 代理拦截 | 绕开，用新浪 + baostock + 腾讯 |
| baostock 报「股票代码应为9位」 | 新浪代码带 `sh/sz/bj` 前缀 | 解析前缀转 `sh.600519`；排除 bj 与 8/4/9 开头 |
| `ashare_data.py` 在原版 Windows 报 `/usr/bin/curl` 不存在 | 硬编码路径 | 用技能自带 `ashare_data_win.py` |
| 22 个 Skill 跑不起来 | 需 Claude Code/Codex + LLM Key | **只静态复用 md + 零依赖 py**，不装运行时 |
| 回测结果对不上 | `END` 硬编码 / 手工录入美股数据 | 不引用、不当本线结果 |

## 7. 铁律与域边界（压过以上一切）

- **只做多、不加杠杆**；A1–A7 全流水线过滤；风控铁闸（单票≤20%、单笔亏损≤2%、同板块≤30%、同时≤5只、环境总仓牛8/熊3/冰点1/退潮0、止损7%取严、止盈2R）。
- **VETO 未解除 → 全批观察档、不打**；龙虎榜 T+1；主力口径禁写「北向净流入」；成本用可复算 vwap20；缺口禁编造。
- 涨=红、跌=绿；货币 ¥；输出带「口径 + 置信度 + 数据缺口 + 免责」四件套，标【模拟】。
- **平行基金**：游锋独立账户由游锋唯一写入；本线只做**非阻塞**风控复核，绝不卡单、绝不改其账目。
- **不碰友军文件**：`ashare-toolset-collab` / `ashare-quant-toolkit` / ETF 域 / 冻结的 `虚拟账户_5000万.md` 一律不改。

## 8. 自我进化（每日）

每日对比前日信号与实际行情写明误判原因；连续 3 天胜率 <60% 或盈亏比明显下滑 → 主动提参数修正建议并附数据支撑；新规律沉淀进 `references/` 与项目 `.workbuddy/memory/YYYY-MM-DD.md`（append-only）。

## 9. 权威文档索引

| 用途 | 路径 |
|---|---|
| 9 款工具全量入口 / 依赖 / 禁用 | `references/9工具速查.md`（本技能） |
| 四道闸逐项检查表 / K-07 字段映射 | `references/落盘质检清单.md`（本技能） |
| 共享库总入口 | `工作区-量化/军团共享数据池/技能与工具仓库/A股量化工具集/机器人调用指引.md`（§6 已含本技能指针） |
| 机器可读索引 | 同目录 `工具索引.json`（v2026-11-05c / 9 款 + 1 技能） |
| AI Berkshire 专项查证 | `工作区-游资/AI-Berkshire-查证与游资用法-20261105-游资.md` |
| 情报全文 / 技能卡 | `工作区-游资/情报吸收-GitHub四大炒股工具-20261105-游资.md`、`共享工具区/游资/游资-GitHub四工具技能卡_v1.0_20261105.md` |
| K-07 输出契约 | `工作区-游资/知识库-K07-输出契约-模板与护栏.md` |
| 铁律全集 | `D:\游资交易日志\规则.md` |
| 版本记录 | `references/CHANGELOG.md` |

> 【模拟】· 工具编排与质检技能，不构成投资建议。VETO 未解除全批观察档，不打。
