---
name: channel-mgmt
description: iptv-api 的频道模板编辑、别名映射、名称匹配技巧。
version: 1.0.0
metadata:
  hermes:
    tags: [iptv, channel-management]
    category: devops
---

# 频道管理

## When to Use
- 用户要增加或删除频道
- 用户说某些频道不出图（匹配失败）
- 用户说要改分类名

## 模板文件
路径：`config/myanmar_sports.txt`

格式：
```ini
⚽ 分类名 Alan公益,#genre#
频道名1
频道名2
```

## 频道名称匹配规则
模板中的频道名必须和订阅源中的频道名**一字不差**才能匹配。

如果用户添加频道后找不到源，大概率是名字对不上。

## 别名映射（解决匹配失败）
文件：`config/alias.txt`

格式：
```ini
模板频道名=源里出现的名字1,源里出现的名字2
```

示例：
```ini
CCTV-Storm Football=CCTV-5 风云足球,Storm Football,风云足球
beIN SPORTS XTRA=beIN Sports XTRA en,beIN XTRA
```

## Procedure

### 添加频道
1. 在 `myanmar_sports.txt` 对应分类下写入频道名
2. 如果频道名和源中的不一样，去 `alias.txt` 加映射
3. 同步到容器 + 重启

### 删除频道
1. **必须用户明确说删才能删**
2. 从 `myanmar_sports.txt` 移除该行
3. 如果 `alias.txt` 有对应映射也删掉
4. 同步到容器 + 重启

### 改分类名
- 直接改 `myanmar_sports.txt` 中 `#genre#` 前面的名字
- 注意保留 "Alan公益" 后缀

## 常见频道来源稳定性
| 频道 | 稳定性 |
|------|--------|
| CCTV-1 ~ CCTV-17 | ⭐⭐⭐⭐⭐ 非常稳定 |
| beIN Sports | ⭐⭐ 付费频道，免费源很少 |
| Sky Sports | ⭐ 基本没有免费源 |
| UFC / WWE / Boxing | ⭐⭐⭐ 偶尔有源 |
| 冷门体育（GLORY、TNA） | ⭐ 基本找不到 |

## Pitfalls
- 频道名别带多余空格，`CCTV-5` 和 `CCTV-5 ` 是两个字
- `alias.txt` 中等号两边不要加空格
- 不要用中文标点

## Verification
- 重启后看 `docker logs --tail 20 iptv-api` 确认匹配了频道
- 访问 `https://iptv.diynets.xyz` 看结果
