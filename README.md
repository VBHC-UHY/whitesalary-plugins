# 🏠 WhiteSalary 插件市场

![插件数量](https://img.shields.io/badge/插件数量-13-blue)
![市场索引](https://img.shields.io/badge/schema-v2-green)
![许可证](https://img.shields.io/badge/license-MIT-yellow)

这是 White Salary 的公开插件仓库。桌面端插件市场、浏览器展示市场和浏览器提交市场都会读取这里的数据。

## 🍃 可用插件

| 插件名称 | 描述 | 角色 | 平台 | 版本 | 作者 | 分类 |
|---------|------|------|------|------|------|------|
| ☀️ 倒数计时 | 计算距离特定日期还有多少天 | 抢答/拦截 / 改写回复 / 提供工具 | all | 1.0.0 | WhiteSalary | 天气日历 |
| 🎮 名言生成 | 随机生成励志名言、毒鸡汤或名人名言 | 抢答/拦截 / 改写回复 / 提供工具 | all | 1.0.0 | WhiteSalary | 娱乐游戏 |
| 📰 天气查询 | 查询全国各地实时天气信息，支持未来天气预报 | 抢答/拦截 / 改写回复 / 提供工具 | all | 1.0.0 | WhiteSalary | 信息 |
| 📦 天气查询插件 | 查询天气信息，支持关键词触发 | 抢答/拦截 / 改写回复 / 提供工具 | all | 1.0.0 | WhiteSalary | utility |
| 💬 彩虹屁生成 | 生成各种花式夸人彩虹屁 | 抢答/拦截 / 改写回复 / 提供工具 | all | 1.0.0 | WhiteSalary | 社交互动 |
| 🌐 快速翻译 | 中英文快速互译 | 抢答/拦截 / 改写回复 / 提供工具 | all | 1.0.0 | WhiteSalary | 翻译语言 |
| 🔧 摸鱼提醒 | 摸鱼人专属！提醒你今天是周几，距离周末还有多久 | 抢答/拦截 / 改写回复 / 提供工具 | all | 1.0.0 | WhiteSalary | 实用工具 |
| 🎮 星座运势 | 查询十二星座今日运势 | 抢答/拦截 / 改写回复 / 提供工具 | all | 1.0.0 | WhiteSalary | 娱乐游戏 |
| 🎮 每日运势 | 每天为用户生成专属运势预测，包括整体运势、爱情、财运等 | 抢答/拦截 / 改写回复 / 提供工具 | all | 1.0.0 | WhiteSalary | 娱乐 |
| 🔧 计算器 | 数学计算器，支持基础运算和科学计算 | 抢答/拦截 / 改写回复 / 提供工具 | all | 1.0.0 | WhiteSalary | 实用工具 |
| 🔧 随机选择 | 帮你做选择！支持多选项随机抽取 | 抢答/拦截 / 改写回复 / 提供工具 | all | 1.0.0 | WhiteSalary | 实用工具 |
| 💬 颜文字生成 | 生成各种可爱的颜文字表情 | 抢答/拦截 / 改写回复 / 提供工具 | all | 1.0.0 | WhiteSalary | 社交互动 |
| 🎮 骰子 | 支持多种骰子的投掷功能，可用于桌游或决策 | 抢答/拦截 / 改写回复 / 提供工具 | all | 1.0.0 | WhiteSalary | 娱乐 |

## 📦 分类统计

- 📦 **utility**: 1 个插件
- 📰 **信息**: 1 个插件
- ☀️ **天气日历**: 1 个插件
- 🎮 **娱乐**: 2 个插件
- 🎮 **娱乐游戏**: 2 个插件
- 🔧 **实用工具**: 3 个插件
- 💬 **社交互动**: 2 个插件
- 🌐 **翻译语言**: 1 个插件

## 🔌 插件目录结构

```text
plugins/<插件ID>/
├── plugin.py       # 主代码
├── config.json     # 插件元数据
├── assets/...      # 可选，图片/模型/音频等资源
├── prompts/...     # 可选，提示词或文本资源
└── README.md       # 可选，插件说明
```

## 🧩 schema v2 元数据

`config.json` 推荐写这些字段：

```json
{
  "schema_version": 2,
  "id": "example_plugin",
  "name": "example_plugin",
  "cn_name": "示例插件",
  "version": "1.0.0",
  "author": "your-name",
  "description": "一句话说明插件做什么",
  "category": "实用工具",
  "roles": ["tool_provider"],
  "platforms": ["qq", "desktop"],
  "permissions": ["owner"],
  "requires_service": ["napcat"],
  "dependencies": {
    "python": ["httpx"]
  },
  "assets": ["assets/icon.png"]
}
```

角色说明：

- `interceptor`: 可通过 `on_message()` 抢答或拦截消息。
- `rewriter`: 可通过 `on_reply()` 改写 AI 最终回复。
- `tool_provider`: 可通过 `get_tools()` 注册工具给 ToolRegistry。
- `observer`: 只通过 `on_observe()` 观察/学习，不抢答、不改写、不注册工具。

旧插件不写 `roles` 也能继续运行，会按 `interceptor + rewriter + tool_provider` 兼容。

## 🚀 提交插件

1. 在线提交：打开 [插件提交页面](https://whitesalary-plugins-web.vercel.app)。
2. 本地同步：在 White Salary WebUI 的插件市场里使用本地同步功能。
3. Pull Request：按 `CONTRIBUTING.md` 的目录结构提交到本仓库。

## ⚠️ 安全边界

- 资源路径只能写插件目录内部的相对路径，不能使用绝对路径或 `..`。
- 权限、依赖服务、Python 依赖只做声明和安装前提示，不会绕过运行时权限与沙箱。
- 插件代码应避免私自读取隐私数据、控制账号或执行高风险操作。

## 📜 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

*最后更新：2026-07-04 03:35*
