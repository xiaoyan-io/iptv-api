---
name: project-rules
description: iptv-api 项目红线 — 明确哪些文件能改、哪些绝不能碰。加载后 Hermes 不会误改框架代码。
version: 1.0.0
metadata:
  hermes:
    tags: [iptv, project-boundaries, safety]
    category: devops
---

# 项目红线

## When to Use
- 用户让你修改 iptv-api 项目的任何代码或配置时
- 不确定某个文件能不能改时

## 绝对禁止修改 🔴
以下文件改一行项目就崩，绝不能碰：

| 路径 | 原因 |
|------|------|
| `main.py` | 主程序入口 |
| `utils/` | 工具模块（constants.py、tools.py 等） |
| `updates/` | 更新逻辑（订阅源获取、EPG、测速） |
| `service/` | Web 服务 |
| `venv/` | Python 虚拟环境 |
| `Pipfile` / `Pipfile.lock` | 依赖声明 |
| `Dockerfile` / `docker-compose.yml` | Docker 部署 |
| `nginx.conf` | Nginx 反向代理 |
| `static/` / `locales/` | 前端静态资源 |
| `config/config.ini` | 默认配置（参考用） |
| `.github/` | CI/CD 工作流 |

唯一例外：`utils/constants.py` 中的 `output_dir` 已被改为 `user_output`（用户已批准）。

## 可以修改 🟡
只改这些文件：

| 文件 | 用途 |
|------|------|
| `config/myanmar_sports.txt` | 频道模板 — 增删频道、改分类名 |
| `config/alias.txt` | 频道别名映射 |
| `config/subscribe.txt` | 订阅源列表（增删 m3u URL） |
| `config/user_config.ini` | 用户配置覆盖 |
| `config/blacklist.txt` | 黑名单 |
| `config/whitelist.txt` | 白名单 |
| `config/local.txt` | 本地源 |

## 硬性规则
1. **不确定能不能改 → 问用户**
2. 改完配置必须 `docker cp` + `docker restart iptv-api`
3. 每次修改必须 `git add` + `git commit` + `git push`
4. 频道名必须和源中**完全一致**才能匹配，不匹配去 `alias.txt` 加别名
5. 不要删已有分类/频道，除非用户明确说

## Pitfalls
- 别手贱改 `config.ini`，那是参考文件，改 user_config.ini 才对
- 修改 `mysports.txt` 模板后如果频道不显示，大概率是频道名和源里不一致

## Verification
- 改完执行 `docker restart iptv-api` 看启动日志无报错
- 访问 `https://iptv.diynets.xyz` 确认结果已更新
