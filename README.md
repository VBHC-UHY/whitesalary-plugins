# 🏪 WhiteSalary 插件市場

![插件數量](https://img.shields.io/badge/插件數量-12-blue)
![版本](https://img.shields.io/badge/版本-1.0.0-green)
![許可證](https://img.shields.io/badge/許可證-MIT-yellow)

專為 白 (WhiteSalary) 打造的官方插件倉庫。在這裡你可以找到各種擴展白功能的插件，也可以分享你自己開發的插件。

## 🍰 可用插件

| 插件名稱 | 描述 | 版本 | 作者 | 分類 |
|---------|------|------|------|------|
| 🎮 骰子游戏 | 掷骰子游戏，支持自定义骰子数量和面数 | 1.0.0 | WhiteSalary | 娱乐游戏 |
| 🔮 每日运势 | 每天为用户生成专属运势预测 | 1.0.0 | WhiteSalary | 娱乐游戏 |
| ⭐ 星座运势 | 查询十二星座今日运势 | 1.0.0 | WhiteSalary | 娱乐游戏 |
| 📜 名言生成 | 随机生成励志名言、毒鸡汤或名人名言 | 1.0.0 | WhiteSalary | 娱乐游戏 |
| ☀️ 天气查询 | 查询指定城市的天气（模拟数据） | 1.0.0 | WhiteSalary | 天气日历 |
| 📅 倒数计时 | 计算距离特定日期还有多少天 | 1.0.0 | WhiteSalary | 天气日历 |
| 🔧 随机选择 | 帮你做选择！支持多选项随机抽取 | 1.0.0 | WhiteSalary | 实用工具 |
| 🐟 摸鱼提醒 | 摸鱼人专属！提醒你今天是周几 | 1.0.0 | WhiteSalary | 实用工具 |
| 🔢 计算器 | 数学计算器，支持基础运算和科学计算 | 1.0.0 | WhiteSalary | 实用工具 |
| 💬 彩虹屁生成 | 生成各种花式夸人彩虹屁 | 1.0.0 | WhiteSalary | 社交互动 |
| 😊 颜文字生成 | 生成各种可爱的颜文字表情 | 1.0.0 | WhiteSalary | 社交互动 |
| 🌐 快速翻译 | 中英文快速互译 | 1.0.0 | WhiteSalary | 翻译语言 |

## 📦 分類統計

- 🎮 **娱乐游戏**: 4 個插件
- 🔧 **实用工具**: 3 個插件
- 💬 **社交互动**: 2 個插件
- ☀️ **天气日历**: 2 個插件
- 🌐 **翻译语言**: 1 個插件

## 🔗 如何安裝插件

### 方法一：通過插件市場（推薦）

1. 啟動 WhiteSalary WebUI
2. 進入「插件市場」頁面
3. 找到想要的插件，點擊「安裝」

### 方法二：手動安裝

1. 下載插件文件夾
2. 放入 WhiteSalary 的 `plugins/` 目錄
3. 重啟白

## 🛠️ 開發你自己的插件

想要為白開發插件？查看我們的 [開發指南](CONTRIBUTING.md)！

### 插件結構

```
your_plugin/
├── plugin.py      # 主代碼文件
└── config.json    # 插件配置
```

### config.json 範例

```json
{
  "id": "my_plugin",
  "cn_name": "我的插件",
  "version": "1.0.0",
  "author": "你的名字",
  "description": "插件描述",
  "category": "实用工具",
  "triggers": ["触发词1", "触发词2"]
}
```

## 📤 提交插件

有兩種方式提交插件：

1. **在線提交**：訪問 [插件提交頁面](https://whitesalary-plugins-web.vercel.app)
2. **本地提交**：在 WhiteSalary WebUI 的「插件市場」頁面點擊「本地提交」

提交後會自動驗證並添加到市場！

## 📜 許可證

MIT License - 詳見 [LICENSE](LICENSE)

---

*最後更新：2026-01-16*
