# enn

A股量化项目集合仓库（monorepo）。聚合基于 **akshare / baostock** 等免费数据源的 A股选股、回测与监控项目，统一归档，便于检索与二次开发。

> 本仓库通过 WorkBuddy 经 GitHub PAT（OAuth 凭证）批量克隆归档，非手工搬运，不使用任何本地旧 token。

## 收录项目

| 目录 | 数据源 | 说明 | 上游仓库 |
|------|--------|------|----------|
| `sequoia-x/` | akshare + baostock | A股自动选股系统：多策略（海龟/均线放量/高窄旗形/涨停洗盘/上升跌停/RPS 突破/定增）+ 飞书推送 | sngyai/Sequoia-X |
| `stock-picker-plus/` | baostock | 智能选股系统：多因子策略、三维评分（基本面+技术面+情绪面）、回测引擎、双格式输出 | striferxu/stock-picker-plus |
| `a-stock-short-term-backtest/` | akshare（新浪接口） | A股短线策略回测：28 套量化策略、多策略共振选股、Flask 控制台 | Leq2468/a-stock-short-term-backtest |

## 目录约定
- 每个子项目置于独立目录，保留其原始 README 与许可证。
- 不纳入归档：`.git`、`__pycache__`、`*.pyc`、`*.pkl`、`data/cache`、锁文件、`docs/`、`tests/`、`MERGE_REPORT.md` 等非核心文件。
- 依赖各自 `requirements.txt` / `pyproject.toml`，运行时各自安装。

## 使用
各子项目独立运行，详见各自目录内的 README。

## 归档记录
- 2026-11-04 通过 GitHub PAT 批量克隆录入：sequoia-x（akshare+baostock）、stock-picker-plus（baostock）、a-stock-short-term-backtest（akshare）。
