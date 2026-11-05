---
name: youzi-github-4tools
description: 游资线收录的 4 款 GitHub A股工具（Sequoia-X / DSA / UZI-Skill / PanWatch）调用技能卡：选票口径、龙虎榜与排雷、盯盘执行纪律、K-07 模板字段映射与红线。供全体机器人友军直接阅读取用。
version: 1.0
author: 游资线（军师代行）
date: 2026-11-05
license: 上游各自 MIT（收录源码保留 LICENSE）
tags: [youzi, a-share, lhb, trap-detection, watchlist, k07, risk]
related_docs:
  - 情报吸收-GitHub四大炒股工具-20261105-游资.md
  - README-工具说明.md
---

# 游资线 · GitHub 四工具技能卡 v1.0

> **给机器人的一句话**：这是一批「候选池 / 排雷 / 盯盘 / 复盘」工具，**不是买卖信号源**。VETO 未解除时，全部只出观察档、不打。
> 上游源码与其自带文档为能力权威；本卡只负责「什么时候用哪个 + 用的时候守住什么」。

---

## 0. 源码在哪（三个落点，任选）

| 落点 | 路径 | 说明 |
|---|---|---|
| **共享技能库（推荐，友军直接读）** | `工作区-量化/军团共享数据池/技能与工具仓库/A股量化工具集/` | 8 款工具源码 + `机器人调用指引.md` + `工具索引.json` |
| **本线仓库（可推送）** | `D:/工作台/2026-10-28-01-23-25/_enn_stage/enn/` | 同 8 款源码 + `dist/` 整包，远端 `github.com/durenjiang/enn` |
| **共享工具区（文档型技能）** | `游资体系总工作台/知识库收集区/共享工具区/游资/` | 本卡 + 情报全文 + README 台账 |

新增两款：`UZI-Skill/`（496 文件 / 11.4 MB）、`PanWatch/`（839 文件 / 20.6 MB），均已剔除 `.git`，密钥扫描 0 命中。

---

## 1. 决策树（先想清楚要什么，再动手）

| 我要… | 用哪个 | 具体入口 | 红线 |
|---|---|---|---|
| 建一份干净的 A 股后复权本地日 K 库 / 扫形态 | **Sequoia-X** | `sequoia-x/main.py --backfill`（首次全量几十分钟），之后 `python main.py` | 作者回测 7 策略**无一超额为正** → 只当候选池生成器 |
| 找「横盘后放量突破 / 缩量回踩」的条件型候选 | **DSA** 的 `volume_breakout` / `shrink_pullback` | `daily_stock_analysis/strategies/`（默认关闭，需手动开） | 排序型前 8 个总会给 Top10，**别把 Top10 当信号**；需自备 LLM Key |
| **判一只票是不是游资票 / 龙虎榜席位是谁 / 同板块辨识度龙头** | **UZI `lhb-analyzer`** | 让 agent 读 `UZI-Skill/skills/lhb-analyzer/SKILL.md` | **龙虎榜 T+1 口径**，不得当同日买入依据 |
| **排雷**（杀猪盘 / 老师荐股 / 异常拉抬） | **UZI `trap-detector`** | 让 agent 读 `UZI-Skill/skills/trap-detector/SKILL.md`，扫全 8 信号并给证据 | 输出 JSON 需附 `trap_score` + 信号证据，不能只给结论 |
| 单票 22 维深研 / 机构方法（DCF / Comps / LBO / IC Memo） | **UZI `deep-analysis`** | `python3 run.py <ticker> --no-browser`；档位 `medium` / `lite` | 深研 ≠ 买卖判断；信息量大、成本高，按需用 |
| 看「66 位大佬分歧」 | **UZI `investor-panel`** | `UZI-Skill/skills/investor-panel/SKILL.md` | **表演性强，只当叙事素材，严禁当信号**（原文作者明确） |
| 后台盯盘 / 价格提醒 / 观察票触发跟踪 | **PanWatch** | 见 `PanWatch/README.zh-CN.md`、`Makefile`、`Dockerfile` | 自托管、数据落本地 SQLite；只做观察档提醒，不开模拟盘下单 |
| 给候选票补「入场 / 目标 / 止损 / 失效 / 归因」字段 | **PanWatch 机会页** | Web 界面机会页候选卡 | 目标价 / 止损价必须过 tickflow 真实成本闸 |
| 验证某策略在真实交易成本下是否还赚钱 | **tickflow-stock-panel** | `backend/app/api/backtest.py`（`fees_pct=0.0002`、`slippage_bps=5`） | 往返成本≈0.19%，保守取 0.30%；本线 5% 动手线已验证无稳定正期望 |

---

## 2. UZI-Skill · 游资线重点两个 skill

根目录 `UZI-Skill/SKILL.md` 自带与本线一致的铁律：**"Do not invent numbers. Use script outputs, cached JSON, or current public evidence."**
游资分析要求 `apply LHB seat matching and is_in_range()`；排雷要求 `scan all eight signals and include concrete evidence when risk is non-trivial`。

| skill | 触发场景 | 输出 | 本线挂接点 |
|---|---|---|---|
| `lhb-analyzer` | 一日游 / 二板 / 核按钮后的席位归因 | markdown 分析 | K-07 护栏「龙虎榜 T+1」；补 A1–A7 的席位复核 |
| `trap-detector` | 入选前排雷、异常放量/荐股型异动 | JSON（trap_score / 证据 / 🟢🟡🟠🔴 评级） | 补**公告排雷 Step0 本地无库**缺口 |

调用姿势（对 agent 说人话即可）：「按 `UZI-Skill/skills/trap-detector/SKILL.md` 对 <代码> 做 8 信号排雷，输出 JSON，每条信号给证据」。
默认数据源无需 API key（akshare / 东财 / 新浪 / 腾讯）；可选 `MX_APIKEY`（东财妙想 Skills Hub 免费 key）让快照更稳，**凭据各线自配，共享层不含任何真实密钥**。

---

## 3. PanWatch · 观察档执行纪律

- **4 个 agent**：盘前分析（开）、收盘复盘（开）、盘中监测（关，手动开）、TradingAgents 深度分析（默认关）。
  → 与本线已配的 09:15 / 14:30 / 15:30 / 22:50 四档**同名同职责**，只作对照，不替代。
- **提醒规则**：价格 / 涨跌幅 / 成交量 / 量比条件，AND/OR 组合，可设仅交易时段、冷却 30 分钟、日上限 3、飞书等通知渠道；自动刷新最少 10s。
  → 本线用于**观察票触发跟踪**，提醒即复核、不即下单。
- **机会页 7 字段**：策略来源、入场区间、目标价、止损价、失效条件、归因（Alpha / 质量 / 催化）、历史样本胜率。

### 字段映射 → K-07 模板2（本线输出契约）

| PanWatch 机会页 | 本线《明日行动票预判》字段 | 状态 |
|---|---|---|
| 策略来源 | ① 选票逻辑 | ✅ 已有（原型①口径） |
| 入场区间 / 目标价 | ② 方向（回踩确认 · 非追高） | ✅ 已有 |
| 历史样本胜率 / 归因 | ③ 可信度 | ✅ 已有（可借此改为**带样本口径**的置信度） |
| 止损价 | ④ 主力成本 vwap20 之下的防守位 | ⚠️ 本线目前只给成本，建议按本卡补「防守位」 |
| **失效条件** | 无 | ❌ **缺口，建议补进模板2** |
| 归因（Alpha/质量/催化） | 无 | ❌ 缺口，可并入选票逻辑 |

> 这是本次情报对**输出契约**最有价值的一处：模板2 目前缺「失效条件」与「止损/防守位」，建议总指挥核准后补入，不擅改 K-07。

---

## 4. 七条红线（每次调用都要过）

1. **禁编造**：所有行情/命中数/胜率必须来自真实接口或本地实跑；文章里的 Star、命中数、278→18 等是**作者口径**，不得写进战报。
2. **只做多、不加杠杆**。
3. **VETO 未解除 → 全批观察档、不打、不落地买卖**；A1–A7 全流水线与风控铁闸缺一环不下单。
4. **龙虎榜 T+1**：席位数据只能用于复盘/次日前置排除，不能当同日买入信号。
5. **主力口径**：不写「北向资金净流入」；主力成本一律用 vwap20 等可复算口径并标注。
6. **真实成本闸**：任何目标价/止损价先过 tickflow 成本模型（往返≈0.19%，保守 0.30%）。
7. **输出四件套**：口径 + 置信度 + 数据缺口 + 免责；标【模拟】，末尾「不构成投资建议」。

---

## 5. 未验证声明（诚实边界）

- 本次仅完成 **源码收录 + 静态阅读（README / SKILL.md）+ 密钥扫描**，**UZI-Skill / PanWatch 均未本地实跑**。
- PanWatch 服务栈较重（Docker / Node / LLM key），UZI 需 Python 依赖；共享层只给源码，**不承诺开箱即跑**。
- 文章提名但未给链接的 Vibe-Trading / go-stock / TradingAgents：**只记线索，不落地**。
- **【18:20 二次增补·修订】AI Berkshire 已查证收录**（`xbtlin/ai-berkshire`，MIT / 22 skills / 共享库第 9 款），专项文档见同目录《AI-Berkshire-查证与游资用法-20261105.md》；要点：**8 条快速否决清单（禁「别人都在买/最近涨得好」追高、禁博傻）+ 镜子测试 5 句话说不清＝不买 + 灰色地带留白** → A1–A7 风控铁闸与 K-07 可信度三态；`financial_rigor.py` 双源校验 / `report_audit.py` 15% 抽检 / `ashare_data_win.py` 腾讯行情（本机实测跑通）→ 禁编造闸门与盘前备用通道；**不是信号源**，四大师结论与自报收益不得进战报。
- 完整转写与裁决见同目录《情报吸收-GitHub四大炒股工具-20261105-游资.md》。

---

*【模拟】· 研究工具与情报转写，不构成投资建议。*
