# AGENTS.md - 项目规则与边界

## 🔴 核心代码（不可修改）

这些文件是框架本身，修改会破坏功能或导致更新失败：

| 路径 | 说明 |
|------|------|
| `main.py` | 主程序入口 |
| `utils/` | 工具模块（constants.py、tools.py、config.py 等） |
| `updates/` | 更新逻辑（订阅源获取、EPG 处理、测速） |
| `service/` | Web 服务 |
| `venv/` | Python 虚拟环境（不要手动修改） |
| `Pipfile` / `Pipfile.lock` | Python 依赖声明 |
| `Dockerfile` / `docker-compose.yml` | Docker 部署配置 |
| `nginx.conf` | Nginx 反向代理配置 |
| `static/` / `locales/` | 前端静态资源和国际化 |

> **例外**: `utils/constants.py` 中的 `output_dir` 变量已被改为 `user_output`，如需改回可修改此项。

---

## 🟡 配置文件（可以修改）

这些是项目的配置和数据，按需编辑：

### 频道管理

| 文件 | 说明 |
|------|------|
| `config/myanmar_sports.txt` | **频道模板** - 增删频道、调整分类 |
| `config/alias.txt` | **频道别名** - 将源中不同名称映射到模板频道名，提高匹配率 |

### 订阅源管理

| 文件 | 说明 |
|------|------|
| `config/subscribe.txt` | **订阅源列表** - 添加/删除 IPTV m3u 源。每行一个 URL。加 `#` 注释可停用 |
| `config/epg.txt` | **EPG 源列表** - 添加/删除节目预告 XML 源 |

### 配置参数

| 文件 | 说明 |
|------|------|
| `config/user_config.ini` | **用户配置** - 覆盖 config.ini 的默认值，主要在此修改 |
| `config/config.ini` | **默认配置** - 所有配置项的完整参考，一般不改 |

### 过滤规则

| 文件 | 说明 |
|------|------|
| `config/blacklist.txt` | 黑名单 - 屏蔽特定接口 URL |
| `config/whitelist.txt` | 白名单 - 强制保留的接口（不参与测速过滤） |
| `config/local.txt` | 本地源 - 手动添加的固定直播链接 |

---

## 🟢 生成文件（由程序自动生成，可删除重新生成）

| 路径 | 说明 |
|------|------|
| `user_output/myanmar_sports_result.txt` | **结果 TXT** - 导入播放器 |
| `user_output/myanmar_sports_result.m3u` | **结果 M3U** - 导入播放器（带台标和 EPG） |
| `user_output/epg/` | EPG 缓存 |
| `user_output/log/` | 运行日志 |
| `output/` | 旧版输出目录（root 权限，不建议使用） |

---

## ⚠️ 重要规则

1. **运行命令**: 必须在 `/home/pi5/iptv-api` 目录下，使用 `venv/bin/python main.py`
2. **虚拟环境**: 不要用系统 Python，必须用 `/home/pi5/iptv-api/venv/bin/python`
3. **输出目录**: `output/` 目录文件为 root 所有，不可写；所有结果在 `user_output/`
4. **更新耗时**: 约 30-50 分钟，取决于网络和测速并发数
5. **频道名称匹配**: 模板中的频道名必须与源中的频道名**完全一致**才能匹配。如不匹配，可：
   - 在 `alias.txt` 中添加别名映射
   - 或修改模板频道名与源一致
6. **付费源**: beIN Sports、Sky Sports 等付费频道在免费源中不存在，需要添加付费订阅源
