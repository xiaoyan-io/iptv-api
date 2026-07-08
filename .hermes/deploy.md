---
name: deploy
description: Docker / nginx / Cloudflare Tunnel 操作指南
---

# 部署操作

## 常用命令
```bash
# 构建镜像
docker build -t iptv-api .

# 启动容器
docker run -d --name iptv-api -p 18010:8000 \
  -v $(pwd)/user_output:/iptv-api/user_output \
  -v $(pwd)/config:/iptv-api/config \
  iptv-api

# 重启容器
docker restart iptv-api

# 查看日志
docker logs -f iptv-api

# 同步配置文件到容器
docker cp config/myanmar_sports.txt iptv-api:/iptv-api/config/myanmar_sports.txt
docker cp config/subscribe.txt iptv-api:/iptv-api/config/subscribe.txt
docker cp config/alias.txt iptv-api:/iptv-api/config/alias.txt
docker cp config/user_config.ini iptv-api:/iptv-api/config/user_config.ini

# 进入容器
docker exec -it iptv-api bash
```

## 配置同步流程
修改配置后：`docker cp` → `docker restart iptv-api`

## 更新结果查看
- `user_output/myanmar_sports_result.txt` — TXT 格式
- `user_output/myanmar_sports_result.m3u` — M3U 格式
- `user_output/log/` — 运行日志

## Cloudflare Tunnel
已在运行中，无需手动操作。网页通过 `https://iptv.diynets.xyz` 访问。
