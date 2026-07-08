---
name: project-rules
description: 项目红线、可改/不可改的文件清单
---

# 项目红线

## 绝对禁止修改
- `main.py`、`utils/`、`updates/`、`service/` — 框架核心
- `Dockerfile`、`docker-compose.yml`、`nginx.conf` — 部署配置
- `venv/`、`Pipfile` — 环境依赖
- `config/config.ini` — 默认配置（参考用）
- `.github/` — CI/CD

## 可以修改
- `config/myanmar_sports.txt` — 频道模板
- `config/alias.txt` — 频道别名映射
- `config/subscribe.txt` — 订阅源列表
- `config/user_config.ini` — 用户配置
- `config/blacklist.txt` — 黑名单
- `config/whitelist.txt` — 白名单
- `config/local.txt` — 本地源

## 硬性规则
1. 不确定能不能改就不要改，先问用户
2. 改完配置必须 `docker cp` 同步到容器 + `docker restart iptv-api`
3. 每次修改必须 `git add` + `git commit` + `git push`
4. 频道名必须和源中**完全一致**才能匹配，不匹配去 `alias.txt` 加映射
5. 不要删已有分类/频道，除非用户明确说
6. 本项目服务于缅甸用户，稳定 > 数量
