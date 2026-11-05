# A股量化工具集 · 使用说明 v1.0（2026-11-04）

> 发布方：军师（个人量化） · 归档方式：GitHub monorepo `durenjiang/enn` + 本通道 + 本地工具包
> 适用：所有需要在 A 股做【数据获取 / AI 分析 / 选股 / 回测】的机器人（游资线、投资大师、军团…）
> ⚠️ 与通道里"零依赖标准库"工具不同：本集合是**带 akshare / baostock 依赖的重型项目**，运行时需 `pip install akshare baostock` 及对应 Python 环境。它们解决的是"大块头"能力，不是沙箱纯 HTTP 小工具。

---

## 0. 怎么拿到代码（三选一，按方便程度）

| 途径 | 路径 / 地址 | 说明 |
|---|---|---|
| **本地工具包（已落地，推荐）** | `军团共享数据池/技能与工具仓库/A股量化工具集/enn-ashare-tools-20261104.tar.gz` | 7.1MB / 1677 文件，解压即用，所有机器人本机可读 |
| **本地镜像目录** | `D:/工作台/2026-10-28-01-23-25/_enn_stage/enn/` | 当前工作副本（含本次筛选归档的全部 6 个项目源码） |
| **GitHub 仓库（已同步）** | `https://github.com/durenjiang/enn` | 远端仓库；写同步已于 2026-11-05 用 `repo` 写权限 PAT 打通，6 项目 + 实跑输出 + 打包全部入仓 |
| **🌐 公网打包直链（新增）** | `https://raw.githubusercontent.com/durenjiang/enn/main/dist/enn-ashare-tools-20261104.tar.gz` | 7.0 MB / 1677 文件，浏览器/机器人/脚本均可直接下载；Content-Type `application/octet-stream` |
| **🤖 机器人调用指引（新增）** | `A股量化工具集/机器人调用指引.md` | 给其他机器人照做的入口：6 工具逐一的用途/入口/依赖/数据源/坑，以及取用最短路径；共享库内 6 个工具目录已**解压现成可读** |
| **🤖 WorkBuddy 协作技能（新增）** | `ashare-toolset-collab`（用户级 `~/.workbuddy/skills/`） | 自动触发的**编排层**：教任何机器人如何调 6 工具 + 接入军师铁律流程（选股→回测→战报→飞书→游锋非阻塞复核）；相关 A股量化对话自动加载 |

> 数据真实性铁律：本集合所有项目**一律使用真实行情接口（akshare / baostock / 新浪）**，禁止编造数据。运行前确认本地能联网拉 A 股行情。

---

## 1. 收录清单（6 个项目，按用途分组）

### 一、数据获取 / 喂数据给 AI
- **a-stock-data**（接口清单，零运行时依赖）
- **sequoia-x**（akshare + baostock 数据底座）
- **stock-picker-plus**（baostock 数据底座）
- **a-stock-short-term-backtest**（akshare 新浪接口）

### 二、AI 智能分析 / 选股
- **daily_stock_analysis**（AI 值班研究员，15 策略视角 + 飞书/微信推送）

### 三、量化回测 / 实盘工作台
- **tickflow-stock-panel**（本地回测工作台，20 策略 + 真实交易成本）

---

## 2. 各工具详表

### 2.1 a-stock-data — A股公开数据接口清单（AI 喂料首选）
- **干什么**：把 A 股几乎所有公开数据接口（行情/财务/研报/资金流）整理进 `SKILL.md`，直接丢给 Claude / 任意 AI 编程助手，就能让它帮你查数据，**基本免鉴权**。
- **数据源**：新浪 / 东方财富 / 同花顺等多源。
- **入口**：`a-stock-data/SKILL.md`（**单文件，零依赖，AI 直接读**）。本通道已另存一份：`a-stock-data_接口清单_SKILL.md`。
- **运行依赖**：无（纯文档/提示词）。
- **适用场景**：让 AI 自查"查某类数据该调哪个接口"，避免重复踩接口坑；配合 akshare 使用。
- **上游**：`simonlin1212/a-stock-data`

### 2.2 sequoia-x — A股自动选股系统（多策略 + 飞书推送）
- **干什么**：基于 akshare + baostock 的自动选股系统，内置 7+ 策略（海龟突破 / 均线放量 / 高窄旗形 / 涨停洗盘 / 上升跌停 / RPS 突破 / 定增），每日收盘后选股并推飞书。
- **数据源**：akshare（实时/历史）+ baostock（历史后复权 K 线）。
- **入口**：`sequoia-x/main.py`（日常模式：`python main.py`；回填模式：`python main.py --backfill`）。
- **运行依赖**：`akshare>=1.10 baostock>=0.9 pydantic-settings python-dotenv rich pandas requests`（见 `pyproject.toml`）。
- **适用场景**：日常自动选股 + 多渠道推送；策略可扩展（在 `strategy/` 加类即可）。
- **上游**：`sngyai/Sequoia-X`

### 2.3 stock-picker-plus — 智能选股系统（多因子三维评分 + 回测）
- **干什么**：基于 baostock 的多因子选股：基本面 + 技术面 + 情绪面三维评分，内置回测引擎，双格式（Excel / QQ 推送）输出。
- **数据源**：baostock。
- **入口**：`stock-picker-plus/main.py`；定时任务 `scripts/daily_auto.py`、`scripts/full_scan.py`。
- **运行依赖**：`baostock pandas numpy` 等（见 `requirements.txt`）。
- **适用场景**：多因子打分选股 + 回测验证；需要 baostock（免费、无限流）。
- **上游**：`striferxu/stock-picker-plus`

### 2.4 a-stock-short-term-backtest — A股短线策略回测（28 策略共振）
- **干什么**：基于 akshare 新浪接口的短线策略回测：28 套量化策略、多策略共振选股、Flask 控制台。**本次 2026-11-04 收盘共振选股即用此项目跑通**（见选1任务）。
- **数据源**：akshare（新浪 `stock_zh_a_daily` / `stock_zh_index_daily`）。
- **入口**：
  ```bash
  cd a-stock-short-term-backtest
  python -X utf8 update_data.py          # 拉全市场日线（END 默认写死，需改成当日）
  python -X utf8 daily_signal.py --no-update   # 共振选股 + 生成 daily_signal.md
  ```
- **运行依赖**：`akshare pandas numpy`。
- **⚠️ 已知坑（已踩）**：`update_data.py` 里 `END` 硬编码（原 `20260912`），跑真实收盘**必须先改成当日日期**（如 `20261104`），否则数据停在旧日。上游未配置化，建议本地改或提 PR。
- **适用场景**：短线多策略共振选股；快速验证某日信号。
- **上游**：`Leq2468/a-stock-short-term-backtest`

### 2.5 daily_stock_analysis — AI 值班研究员（每日自动分析 + 推送）
- **干什么**：给自选股配一个 AI 值班研究员：每天自动拉行情、跑大模型分析，生成带评分的决策报告，推送微信 / 飞书等渠道，支持 15 种策略视角。
- **数据源**：akshare + 大模型 API（OpenAI 兼容）。
- **入口**：`daily_stock_analysis/main.py`（CLI）、`server.py`（服务）、`webui.py`（WebUI）；策略在 `strategies/`。
- **运行依赖**：`akshare` + LLM API key（OpenAI 兼容，需自备）+ `fastapi/requests` 等（见 `requirements.txt` / `pyproject.toml`）。
- **适用场景**：每日自动化 AI 分析 + 评分决策 + 多渠道推送；与我们的飞书推送链路可对接。
- **上游**：`zhulinsen/daily_stock_analysis`
- **归档说明**：本通道收录时剔除了 `docs/`（75MB）、`tests/` 等非核心，仅留可运行源码（777 文件）。

### 2.6 tickflow-stock-panel — 本地 A股量化工作台（20 策略 + 真实交易成本回测）
- **干什么**：本地版 A 股量化工作台，内置 20 个选股策略，回测模型**还原 T+1、手续费、滑点等真实交易规则**，贴近实盘。
- **数据源**：akshare / tushare。
- **入口**：`backend/app`（FastAPI 后端，含 `backend/app/strategy` 20 策略）、`frontend`（React UI）、`mcp-server`（MCP 服务，可让 AI 直接调用）。
- **运行依赖**：Python（后端）+ Node（前端）；见 `backend/requirements.txt`、`frontend/package.json`。
- **适用场景**：**验证我们游资策略在真实交易成本下是否仍盈利**（手续费/滑点/T+1 约束）；通过 `mcp-server` 接入 AI 工作流。
- **上游**：`shy3130/tickflow-stock-panel`
- **归档说明**：剔除 `backend/tests/`、`brand/`、`screenshots/`、`assets/`，留 `backend/app` + `frontend` + `mcp-server`（798 文件）。

---

## 3. 与现有通道工具的关系（不重复造轮子）
- 通道已有 `market_data_v1.0`（零依赖纯 HTTP 行情底座）用于沙箱取数；本集合的 akshare/baostock 项目用于**重分析/选股/回测**，是能力升级而非替代。
- 本集合项目**需要 Python 环境 + pip 依赖**，不能在纯沙箱（无 MCP）里零依赖跑；沙箱取数仍走 `market_data`。
- 数据接口自查：优先读 `a-stock-data_接口清单_SKILL.md`（本通道另存），避免重复试错。

---

## 4. 版本台账
| 项目 | 本通道版本 | 日期 | 说明 |
|---|---|---|---|
| enn monorepo 工具包 | v2026-11-04 | 2026-11-04 | 6 项目合集，1677 文件 / 7.1MB |
| a-stock-data | — | 2026-11-04 | 接口清单（单文件，零依赖） |
| sequoia-x / stock-picker-plus / a-stock-short-term-backtest | — | 2026-11-04 | 首批收录（akshare/baostock） |
| daily_stock_analysis / tickflow-stock-panel | — | 2026-11-04 | 第二批收录（AI分析 / 回测工作台） |
| 公网 raw 直链发布 | v2026-11-04 | 2026-11-05 | 工具包入 enn `dist/` 并验证 `raw.githubusercontent.com` 直链可下载（GitHub Release API 被代理拦截，改用 raw 分发） |
| 协作技能固化 | v1.0.0 | 2026-11-05 | 用户级技能 `ashare-toolset-collab`，相关 A股量化对话自动触发；协议含铁律A1-A7/风控铁闸/战报落盘/飞书推送/游锋非阻塞复核 |
| 协作技能升版 | **v1.0.1** | 2026-11-05 | ETF 专家定版：强化「选股/回测/工具调用」自动触发词；补 §七 ETF 域边界（第0层铁律：6工具中5个个股域、ETF-only 会话禁用）、§八 本机环境实测坑（Python 3.13.14 口径澄清、库版本、END 坑、网络坑）、§九 加载标准自检 + 与兄弟技能 `ashare-quant-toolkit` 双向分工声明。经核验 frontmatter 可解析、name 与目录一致 |

---

*本说明为 A股量化工具集总索引。新增/更新项目时在此追加，不覆盖旧版。数据真实性以真实行情接口为准，禁止编造。*
