# 🏪 WhiteSalary 插件市場

<p align="center">
  <img src="https://img.shields.io/badge/插件数量-3-blue" alt="Plugins">
  <img src="https://img.shields.io/badge/版本-1.0.0-green" alt="Version">
  <img src="https://img.shields.io/badge/许可证-MIT-orange" alt="License">
</p>

專為 **白 (WhiteSalary)** 打造的官方插件倉庫。在這裡你可以找到各種擴展白功能的插件，也可以分享你自己開發的插件。

## 📦 可用插件

| 插件名稱 | 描述 | 版本 | 作者 |
|---------|------|------|------|
| 🔮 每日運勢 | 每天為用戶生成專屬運勢預測 | 1.0.0 | WhiteSalary |
| 🌤️ 天氣查詢 | 查詢全國各地實時天氣信息 | 1.0.0 | WhiteSalary |
| 🎲 骰子 | 支持多種骰子的投擲功能 | 1.0.0 | WhiteSalary |

## 🚀 如何安裝插件

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
├── plugin.py      # 主程序文件（必需）
├── config.json    # 插件配置（必需）
└── README.md      # 說明文檔（可選）
```

### 提交插件
1. Fork 本倉庫
2. 在 `plugins/` 目錄下創建你的插件文件夾
3. 提交 Pull Request
4. 等待自動審核通過後自動上架！

## 📄 許可證

MIT License - 詳見 [LICENSE](LICENSE)

---

<p align="center">
  Made with ❤️ for 白
</p>


