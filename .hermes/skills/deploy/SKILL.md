---
name: deploy
description: iptv-api 的 Docker 操作、配置同步、重启、查看日志的完整流程。
version: 1.0.0
metadata:
  hermes:
    tags: [iptv, docker, devops]
    category: devops
---

# 部署操作

## When to Use
- 用户改了配置后要同步到容器
- 容器出问题要重启或看日志
- 检查更新是否运行正常

## 容器信息
- 容器名：`iptv-api`
- 镜像端口映射：`18010:8000`
- 网页地址：`https://iptv.diynets.xyz`

## Procedure

### 1. 同步配置到容器
```bash
docker cp config/myanmar_sports.txt iptv-api:/iptv-api/config/myanmar_sports.txt
docker cp config/subscribe.txt iptv-api:/iptv-api/config/subscribe.txt
docker cp config/alias.txt iptv-api:/iptv-api/config/alias.txt
docker cp config/user_config.ini iptv-api:/iptv-api/config/user_config.ini
```

### 2. 重启容器
```bash
docker restart iptv-api
```

### 3. 查看启动日志（确认没问题）
```bash
docker logs --tail 20 iptv-api
```

### 4. 查看更新进度（如果 main.py 正在跑）
```bash
docker logs -f iptv-api
```

### 5. 查看生成结果
```bash
# TXT 格式
cat user_output/myanmar_sports_result.txt

# M3U 格式
cat user_output/myanmar_sports_result.m3u
```

## 更新耗时
- 测速开启（`open_speed_test = True`）：30-50 分钟
- 测速关闭：5-10 分钟

## Pitfalls
- 别用 `output/` 目录，那是 root 权限的旧版目录，写不进去
- 所有生成结果在 `user_output/`
- 容器重启后如果马上看日志可能还没启动完，等 3-5 秒

## Verification
- `docker ps` 确认容器状态是 `Up`
- 浏览器访问 `https://iptv.diynets.xyz` 看看能不能打开
