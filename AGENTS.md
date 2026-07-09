# AGENTS.md - 项目规则与边界（AI 请严格遵循）

> 你是 AI 助手，你的职责是辅助，不是重构。
> **如果你不确定能不能改，就不要改。先问用户。**

---

## 🔴 禁止触碰（绝不可修改）

这些文件是框架本身。**修改任何一行都会破坏项目，导致不可用。**

| 路径 | 说明 |
|------|------|
| `main.py` | 主程序入口 |
| `utils/` | 工具模块（constants.py、tools.py、config.py 等） |
| `updates/` | 更新逻辑（订阅源获取、EPG 处理、测速） |
| `service/` | Web 服务 |
| `venv/` | Python 虚拟环境 |
| `Pipfile` / `Pipfile.lock` | Python 依赖声明 |
| `Dockerfile` / `docker-compose.yml` | Docker 部署配置 |
| `static/` / `locales/` | 前端静态资源和国际化 |
| `config/config.ini` | 默认配置（参考用，不要改） |
| `.github/` | CI/CD 工作流 |

**即使你觉得"这行代码没用"、"这个看起来像 bug"、"我想优化一下"——也不准改。** 除非用户明确要求。

> 唯一例外：`utils/constants.py` 中的 `output_dir` 变量已被改为 `user_output`，如需改回可修改此项。

---

## 🟡 可以修改的文件

只改这些文件，其他都不准动：

### 频道管理

| 文件 | 说明 | 允许操作 |
|------|------|----------|
| `config/myanmar_sports.txt` | **频道模板** | 增删频道、改分类名、调整频道顺序 |
| `config/alias.txt` | **频道别名** | 添加/修改频道名称映射（提高匹配率） |

### 订阅源管理

| 文件 | 说明 | 允许操作 |
|------|------|----------|
| `config/subscribe.txt` | **订阅源列表** | 添加/删除/注释 m3u 源 |
| `config/epg.txt` | **EPG 源列表** | 添加/删除节目预告 XML 源 |

### 配置参数

| 文件 | 说明 | 允许操作 |
|------|------|----------|
| `config/user_config.ini` | **用户配置** | 覆盖默认配置（测速开关、并发数等） |

### 过滤规则

| 文件 | 说明 | 允许操作 |
|------|------|----------|
| `config/blacklist.txt` | **黑名单** | 添加要屏蔽的接口 URL |
| `config/whitelist.txt` | **白名单** | 添加强制保留的接口 |
| `config/local.txt` | **本地源** | 添加手动固定的直播链接 |

### Nginx 与服务路由

| 文件 | 说明 | 允许操作 |
|------|------|----------|
| `nginx.conf` | **Nginx 反向代理** | 添加新工具路由（`location /xxx/`）、修改代理规则 |
| `nginx.conf.template` | **Nginx 模板** | 同上，保持与 `nginx.conf` 同步 |

### 首页仪表盘

| 文件 | 说明 | 允许操作 |
|------|------|----------|
| `user_output/index.html` | **服务仪表盘首页** | 添加/修改工具卡片、更新 TOOLS 数组 |

---

## 🟢 生成文件（程序自动生成，不要手动编辑）

| 路径 | 说明 |
|------|------|
| `user_output/`（除 index.html 外） | 所有生成结果、日志、EPG 缓存 |
| `output/` | 旧版输出目录（root 权限，不可写） |

---

## 🏗️ 仪表盘与工具系统

项目已扩展为 **IPTV + AI 工具门户**，首页是统一仪表盘（`user_output/index.html`）。

### 工具部署流程

添加新工具分 4 步：

1. **准备 HTML 文件** — 单页应用，保存为 `user_output/<工具名>/index.html`
2. **添加 nginx 路由** — 在 `nginx.conf` 和 `nginx.conf.template` 中添加：
   ```
   location /工具名/ {
       root /iptv-api/user_output;
   }
   ```
3. **注册到仪表盘** — 在 `user_output/index.html` 的 `TOOLS` 数组中添加一条：
   ```js
   {icon:'📄', name:'工具名称', desc:'简短描述', href:'/工具名', color:'#1a2a3a'},
   ```
4. **同步容器** — `docker cp` + `docker exec nginx -s reload`

### nginx 路由规则

- **动态反向代理**：`/iptv` → `proxy_pass` 到 gunicorn（5180 端口）
- **静态文件工具**：`/xxx/` → `root /iptv-api/user_output`，自动服务 `index.html`
- 新工具统一用静态文件模式

---

## ⚠️ 硬性规则

1. **不要修改框架代码** — 任何 `main.py`、`utils/`、`updates/`、`service/` 下的文件都不准动
2. **运行命令**：必须在 `/home/pi5/iptv-api` 下，用 `venv/bin/python main.py`
3. **不要用系统 Python**，必须用 `venv/bin/python`
4. **结果路径**：`user_output/`，不是 `output/`
5. **更新耗时**：30-50 分钟（测速开启后可能更久）
6. **频道名称必须精确匹配** 源中的频道名才能被识别，不匹配时去 `alias.txt` 加映射
7. **如果用户问"你觉得呢"、"你的建议是"** — 先分析利弊，把选项列出来，让用户决定，不要擅自改
8. **每次改完配置，必须同步到容器**：`docker cp nginx.conf iptv-api:/etc/nginx/nginx.conf` + `docker exec iptv-api nginx -s reload`
9. **改完要 `git add`、`git commit`、`git push`** 到对应的分支
10. **不要删除已有的分类或频道**，除非用户明确说"删掉"
11. **添加新频道时**，命名要和在源中出现的一致，否则匹配不上
12. **nginx.conf 和 nginx.conf.template 必须同步修改**

---

## 📌 项目定位

- 本项目是 **运行在 Raspberry Pi 5 上的 IPTV 聚合服务 + AI 工具门户**
- 服务的用户位于 **缅甸**，网络延迟较高
- 所有产出通过 **Docker + Nginx + Cloudflare Tunnel** 对外提供
- 核心目标：**稳定 > 数量**，优先保证亚洲地区可用的节点
- 工具系统：浏览器端纯静态，无后端依赖，数据不离开设备
