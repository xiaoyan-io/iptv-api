---
name: git-workflow
description: 提交规范与分支策略
---

# Git 工作流

## 当前分支
`feature/myanmar-sports-ui`

## 提交流程
```bash
git add <改过的文件>
git commit -m "简短描述改了什么"
git push
```

## commit 规范
```
操作：具体内容
```
示例：
- `添加CCTV-5别名映射，提升匹配率`
- `精简频道：删除不稳定的MLB Channel`
- `开启测速选最优源，添加亚洲IPTV源`

不要写英文 commit，用户是中文用户。

## 重要
- commit 前确认只 stage 了要提交的文件
- 不要 --force-push
- 不要改别人的 commit 历史
