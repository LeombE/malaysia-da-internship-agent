# Malaysia Data Analyst Internship Agent

目标：每天 2 次自动收集、去重、评分并发送马来西亚 Data Analyst / Analytics / BI 相关 internship 机会，重点地区：Johor、Selangor、Kuala Lumpur、Penang。默认实习窗口按 **2026-08-02 到 2026-11-03**，约 3 个月；如果职位要求超过 3 个月，也会保留但降低日期匹配分。

> 合规原则：优先使用 Jobs API、Google Alerts、公司官网公开 career pages；不要绕过登录、验证码、反爬或平台限制；不要抓取个人资料。

## 1. 文件结构

```text
.
├── .github/workflows/daily.yml       # GitHub Actions：每天 08:30 + 20:30 MYT 执行
├── config.yml                        # 地区、关键词、公司分层、评分权重
├── .env.example                      # 需要配置的密钥
├── requirements.txt
├── data/company_targets.yml          # 大公司/目标公司 career page 配置
├── prompts/codex_morning.md          # 每天第 1 次 Codex prompt
├── prompts/codex_evening.md          # 每天第 2 次 Codex prompt
└── src/
    ├── main.py                       # 主入口
    ├── models.py                     # JobPosting 数据模型
    ├── scoring.py                    # 评分逻辑
    ├── storage.py                    # SQLite 去重与历史记录
    ├── notifications.py              # Telegram / Email 通知
    └── sources/
        ├── jsearch.py                # JSearch API
        ├── adzuna.py                 # Adzuna API
        ├── google_alerts.py          # Google Alerts RSS/Atom
        └── company_pages.py          # 公司官网公开页面，robots-respectful
```

## 2. 本地安装

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
```

编辑 `.env`，最少建议先配置：

```bash
JSEARCH_API_KEY=...
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

Adzuna、Google Alerts、SMTP email 都是可选；没有配置的 source 会自动跳过。

## 3. 运行测试

```bash
python -m src.main --dry-run
```

成功后你会看到：

- SQLite 数据库：`data/jobs.db`
- CSV 导出：`data/latest_ranked_jobs.csv`
- 控制台输出 top results

正式发送：

```bash
python -m src.main
```

## 4. GitHub Actions 部署

1. 新建 GitHub repo，例如 `malaysia-da-internship-agent`。
2. 把本项目文件 push 上去。
3. 进入 GitHub repo → Settings → Secrets and variables → Actions → New repository secret。
4. 添加 `.env.example` 里的密钥，例如：
   - `JSEARCH_API_KEY`
   - `ADZUNA_APP_ID`
   - `ADZUNA_APP_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `SMTP_HOST`
   - `SMTP_PORT`
   - `SMTP_USER`
   - `SMTP_PASS`
   - `EMAIL_TO`
5. 打开 Actions tab，手动点 Run workflow 测试一次。

默认计划：每天马来西亚时间 08:30 和 20:30 运行。GitHub Actions 使用 UTC cron，所以 workflow 里写的是 `30 0,12 * * *`。

## 5. Google Alerts 设置

建议创建这些 Alerts，然后把 RSS feed URL 放进 `.env` 的 `GOOGLE_ALERT_FEEDS`，用逗号分隔：

```text
"data analyst intern" Malaysia
"data analytics internship" Malaysia
"business intelligence intern" Malaysia
"data science internship" Malaysia
"Power BI intern" Malaysia
"SQL intern" Malaysia
"data analyst internship" "Kuala Lumpur"
"data analyst internship" Selangor
"data analyst internship" Penang
"data analyst internship" Johor
"latihan industri" "data analyst" Malaysia
"praktikal" "data analytics" Malaysia
site:careers.* Malaysia "data analyst intern"
```

## 6. Codex 每天 2 次使用方式

不要让 Codex 每天“手动浏览网页”来消耗 token；那样不稳定，也不利于复现。更好的 token 策略是：

- 早上：让 Codex 检查昨晚/今早的 run logs、失败 source、低质量结果，自动修采集器和 query。
- 晚上：让 Codex 根据 `latest_ranked_jobs.csv`、`jobs.db` 和你的申请状态，改进评分、补目标公司、产出明天申请清单。

复制 `prompts/codex_morning.md` 和 `prompts/codex_evening.md` 到 Codex 使用。

## 7. 数据质量规则

每条职位必须尽量保留：

- source, source_url, apply_url
- title, company, location, state
- description / snippet
- posted_at, first_seen_at, last_seen_at
- role_fit_score, date_fit_score, location_score, company_tier_score, total_score
- reason: 为什么推荐/为什么降权

## 8. 申请优先级

- A：官方公司 career page + 大公司/结构化 internship + 明确 3 个月或可协商 + 地点匹配。
- B：大型平台/API 聚合 + 描述高度匹配 + 无明确日期但 internship 合理。
- C：小公司/SME + 明确接受 internship + 任务含 Excel/SQL/Power BI/Python。
- D：全职、senior、manager、明显不收 intern、地点不匹配、需要 6 个月且不可协商。
