# enn

A股量化项目集合仓库（monorepo）。聚合基于 **akshare / baostock** 等免费数据源的 A股选股、回测、AI 分析与数据接口项目，统一归档，便于检索与二次开发。

> 本仓库通过 WorkBuddy 经 GitHub PAT 批量克隆归档，非手工搬运，不使用任何本地旧 token。归档时对上游仓库做了精简：剔除 `docs/`、`tests/`、`screenshots/`、`assets/`、`brand/` 等非核心内容，仅保留可运行的源码与配置，保持仓库精干。

## 收录项目

### 一、AI 智能分析与选股
| 目录 | 数据源 | 说明 | 上游仓库 |
|------|--------|------|----------|
| `daily_stock_analysis/` | akshare / 大模型 | AI 值班研究员：每天自动拉行情 + 跑大模型分析，生成带评分的决策报告并推送微信/飞书，支持 15 种策略视角 | zhulinsen/daily_stock_analysis |

### 二、全栈数据获取（喂数据给 AI）
| 目录 | 数据源 | 说明 | 上游仓库 |
|------|--------|------|----------|
| `a-stock-data/` | 多源（新浪/东财等） | 把 A 股公开数据接口整合进 `SKILL.md`，直接丢给 Claude 等 AI 助手即可查行情/研报/资金流，基本免鉴权 | simonlin1212/a-stock-data |
| （依赖）`akshare` | 多源 | Python 界全能型数据接口库（行情/财务/资金流），免费免注册；作为各子项目的 pip 依赖使用，不在此 vendoring 源码 | akfamily/akshare |

### 三、量化回测与本地工作台
| 目录 | 数据源 | 说明 | 上游仓库 |
|------|--------|------|----------|
| `tickflow-stock-panel/` | akshare / tushare | 本地 A 股量化工作台：内置 20 个选股策略，回测还原 T+1/手续费/滑点等真实交易规则 | shy3130/tickflow-stock-panel |
| `sequoia-x/` | akshare + baostock | A股自动选股系统：多策略（海龟/均线放量/高窄旗形/涨停洗盘/上升跌停/RPS 突破/定增）+ 飞书推送 | sngyai/Sequoia-X |
| `stock-picker-plus/` | baostock | 智能选股系统：多因子策略、三维评分（基本面+技术面+情绪面）、回测引擎、双格式输出 | striferxu/stock-picker-plus |
| `a-stock-short-term-backtest/` | akshare（新浪接口） | A股短线策略回测：28 套量化策略、多策略共振选股、Flask 控制台 | Leq2468/a-stock-short-term-backtest |

## 目录约定
- 每个子项目置于独立目录，保留其原始 README 与许可证。
- 不纳入归档：`.git`、`__pycache__`、`*.pyc`、`*.pkl`、`data/cache`、锁文件、`docs/`、`tests/`、`screenshots/`、`assets/`、`brand/`、`MERGE_REPORT.md` 等非核心文件。
- 依赖各自 `requirements.txt` / `pyproject.toml`，运行时各自安装。

## 使用
各子项目独立运行，详见各自目录内的 README。

## 发布与下载
- **公网打包下载（推荐机器人/本机直链）**：`https://raw.githubusercontent.com/durenjiang/enn/main/dist/enn-ashare-tools-20261104.tar.gz`
  - 7.0 MB / 1677 文件，解压即用；Content-Type 为 `application/octet-stream`，浏览器与脚本均可直接下载。
  - 本地镜像：`D:/工作台/游资体系总工作台/工作区-量化/军团共享数据池/技能与工具仓库/A股量化工具集/enn-ashare-tools-20261104.tar.gz`
- GitHub Release API 在本环境被网络代理拦截，故采用 `dist/` 目录 + raw 直链方式分发，等效于可下载发布物。

## 归档记录
- 2026-11-04（第一批）：sequoia-x（akshare+baostock）、stock-picker-plus（baostock）、a-stock-short-term-backtest（akshare）。
- 2026-11-04（第二批）：daily_stock_analysis（AI 分析）、a-stock-data（数据接口 skill）、tickflow-stock-panel（回测工作台）。
