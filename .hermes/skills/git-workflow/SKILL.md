---
name: git-workflow
description: iptv-api 项目的 git 提交流程、commit 规范、当前分支信息。
version: 1.0.0
metadata:
  hermes:
    tags: [iptv, git, workflow]
    category: devops
---

# Git 工作流

## When to Use
- 修改了项目文件需要提交
- 用户说"提交"或"push"

## 当前分支
`feature/myanmar-sports-ui`

## Procedure

```bash
# 1. 暂存改过的文件
git add config/myanmar_sports.txt
git add config/alias.txt
# 或者全部
git add -A

# 2. 提交（写中文，不要写英文）
git commit -m "简短描述改了什么"

# 3. 推送到远程
git push
```

## Commit 规范
commit 信息用中文，简洁明了：

| 好 | 不好 |
|----|------|
| 添加CCTV-5别名映射 | update config |
| 精简频道：删除不稳定源 | fix things |
| 开启测速选最优源 | changes |

## Pitfalls
- 不要 `--force-push` 或 `--amend`
- commit 前确认只 stage 了要改的文件（用 `git status` 检查）
- 不要修改其他人的 commit 历史
- 不要在这个分支上 merge master

## Verification
- `git log --oneline -3` 确认最新提交包含你的修改
- `git status` 确认工作区干净
