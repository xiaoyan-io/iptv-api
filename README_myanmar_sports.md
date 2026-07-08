# 缅甸体育直播源使用说明

## 简介

基于 iptv-api 自动采集、筛选、测速，生成缅甸可用的体育直播源（txt/m3u 格式），导入播放器即可观看。

## 快速使用

### 更新直播源

```bash
cd /home/pi5/iptv-api
/home/pi5/iptv-api/venv/bin/python main.py
```

更新耗时约 30-50 分钟（取决于网络和测速并发数）。

### 结果文件

- **TXT 格式**: `user_output/myanmar_sports_result.txt`
- **M3U 格式**: `user_output/myanmar_sports_result.m3u`

## 当前频道 (2026-07-07)

### ✅ 有可用源的频道

| 分类 | 频道 |
|------|------|
| ⚽ Sports | CCTV-5、CCTV-5+、CCTV-16、CCTV-8K |
| 🏆 Football | LaLiga TV、FIFA+ |
| 🌏 Asian Sports | MCOT HD、Thairath TV、Channel 8、One 31、GMM 25 |
| 📺 Sports News | CCTV-13、CGTN、CGTN Documentary、NHK World-Japan、CNN |
| 💪 Fighting & Wrestling | WWE Superstar Central |
| 📺 International Sports | Women's Sports Network |

### ❌ 暂无源的频道（需添加付费订阅源）

beIN Sports 系列、Sky Sports 系列、Premier League 系列、Astro Supersport 系列、True Sport 系列、UFC、ESPN 等

## 自定义频道列表

编辑 `config/myanmar_sports.txt`，格式如下：

```
⚽ Sports,#genre#
CCTV-5
CCTV-5+

🏆 Football,#genre#
FIFA+
LaLiga TV
```

- `#genre#` 表示分类标题
- 每行一个频道名称
- 系统会从订阅源中自动匹配同名频道

## 添加订阅源

编辑 `config/subscribe.txt`，每行一个 m3u 订阅链接：

```
https://example.com/iptv.m3u
```

加 `#` 注释可临时停用。

## 添加 EPG 节目预告

编辑 `config/epg.txt`，每行一个 EPG XML 链接：

```
https://example.com/epg.xml
```

## 配置说明

主要配置在 `config/user_config.ini`（会覆盖 `config.ini` 的同名配置）：

| 配置 | 值 | 说明 |
|------|-----|------|
| source_file | config/myanmar_sports.txt | 频道模板 |
| final_file | user_output/myanmar_sports_result.txt | 结果输出路径 |
| time_zone | Asia/Yangon | 缅甸时区 |
| min_resolution | 640x480 | 最低分辨率 |
| min_speed | 0.2 | 最低速率 M/s |
| urls_limit | 5 | 每频道保留接口数 |
| speed_test_timeout | 5 | 测速超时(秒) |
| open_epg | True | 开启节目预告 |
| open_m3u_result | True | 生成 M3U 格式 |

## 播放器

推荐播放器：
- **TiviMate** (Android TV)
- **IPTV Smarters** (Android/iOS)
- **VLC** (全平台)
- **PotPlayer** (Windows)

在播放器中导入 `user_output/myanmar_sports_result.m3u` 或 `user_output/myanmar_sports_result.txt` 即可。

## 项目结构

```
config/
├── myanmar_sports.txt    # 频道模板（编辑此文件增减频道）
├── subscribe.txt         # 订阅源列表（添加更多源）
├── epg.txt              # EPG 源列表
├── alias.txt            # 频道别名映射
├── user_config.ini      # 个性化配置
└── config.ini           # 默认配置

user_output/
├── myanmar_sports_result.txt  # 结果 TXT
├── myanmar_sports_result.m3u  # 结果 M3U
└── epg/                      # EPG 缓存

venv/  # Python 虚拟环境
```
