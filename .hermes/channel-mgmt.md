---
name: channel-mgmt
description: 增删频道、别名映射、匹配技巧
---

# 频道管理

## myanmar_sports.txt 格式
```ini
⚽ 分类名 Alan公益,#genre#
频道1
频道2
```

## 频道名称匹配规则
- 模板中的频道名必须和源中的频道名**一字不差**才能匹配
- 如果不匹配，去 `alias.txt` 加别名映射

## alias.txt 格式
```ini
模板频道名=源中的频道名1,源中的频道名2
```
示例：
```ini
CCTV-Storm Football=CCTV-5 风云足球,CCTV风云足球,Storm Football
beIN SPORTS XTRA=beIN SPORTS XTRA en,beIN Sports XTRA
```

## 添加新频道的步骤
1. 在 `myanmar_sports.txt` 对应分类下添加频道名
2. 如果源中名称不同，在 `alias.txt` 添加映射
3. 同步到容器并重启

## 删除频道的步骤
1. 用户明确说要删才能删
2. 从 `myanmar_sports.txt` 中移除该行
3. 如果 `alias.txt` 有对应映射也一起删

## 来源稳定性（经验）
- CCTV 系列（CCTV-1 ~ CCTV-17）— 非常稳定，基本都有源
- beIN Sports / Sky Sports — 付费频道，免费源很少能找到
- 小众体育（GLORY、TNA）— 基本找不到稳定源
