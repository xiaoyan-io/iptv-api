# Hermes Skills for iptv-api

## 安装

在 `~/.hermes/config.yaml` 中添加：

```yaml
skills:
  external_dirs:
    - /home/pi5/iptv-api/.hermes/skills
```

然后运行 `hermes skill update` 即可加载。

## Skills

- `/project-rules` — 项目红线，能改/不能改的文件清单
- `/deploy` — Docker 操作、配置同步、重启
- `/channel-mgmt` — 频道编辑、别名映射
- `/git-workflow` — 提交流程、commit 规范
