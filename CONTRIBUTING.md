# 贡献插件说明

这个仓库是 White Salary 的公开插件市场数据源。浏览器展示市场、浏览器上传市场、桌面端插件市场都会读取这里的 `plugins.json` 和 `plugins/<插件ID>/`。

## 插件应该放哪里

标准目录：

```text
plugins/<plugin_id>/
├── plugin.py       # 必需，插件主代码
├── config.json     # 必需，插件元数据
├── assets/...      # 可选，图片/模型/音频等资源
├── prompts/...     # 可选，提示词或文本资源
└── README.md       # 可选，插件说明
```

`plugin_id` 只能使用小写字母、数字、下划线，并且必须以字母开头，例如 `daily_fortune`。

## 当前插件接口

请使用当前 White Salary 接口，不要使用旧的 `src.core.plugins.base.BasePlugin`。

最小示例：

```python
# -*- coding: utf-8 -*-
from typing import Optional

from white_salary.core.plugins.base import Plugin, PluginMeta


class ExamplePlugin(Plugin):
    meta = PluginMeta(
        name="example_plugin",
        version="1.0.0",
        author="your-name",
        description="示例插件",
        roles=["interceptor"],
    )

    async def on_message(self, text: str, user_id: str = "") -> Optional[str]:
        if "示例" in text:
            return "这是插件回复"
        return None


Plugin = ExamplePlugin
```

## 插件角色

`roles` 用来告诉运行时这个插件参与哪一段链路。

| 角色 | 作用 |
|------|------|
| `interceptor` | 通过 `on_message()` 抢答或拦截用户消息 |
| `rewriter` | 通过 `on_reply()` 改写 AI 最终回复 |
| `tool_provider` | 通过 `get_tools()` 注册工具给 ToolRegistry |
| `observer` | 通过 `on_observe()` 观察/学习消息，不抢答、不改写、不注册工具 |

旧插件不写 `roles` 时，会按 `interceptor + rewriter + tool_provider` 兼容运行。

工具插件示例：

```python
from white_salary.core.plugins.base import Plugin, PluginMeta


class RollDicePlugin(Plugin):
    meta = PluginMeta(
        name="roll_dice",
        version="1.0.0",
        author="your-name",
        description="骰子工具",
        roles=["tool_provider"],
    )

    def get_tools(self):
        return [
            {
                "name": "roll_dice",
                "description": "掷一个指定面数的骰子",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sides": {"type": "integer", "description": "骰子面数"}
                    },
                    "required": ["sides"],
                },
                "handler": self.roll_dice,
            }
        ]

    async def roll_dice(self, sides: int = 6):
        import random
        return random.randint(1, max(2, int(sides)))


Plugin = RollDicePlugin
```

观察插件示例：

```python
from white_salary.core.plugins.base import Plugin, PluginMeta


class MoodObserverPlugin(Plugin):
    meta = PluginMeta(
        name="mood_observer",
        version="1.0.0",
        author="your-name",
        description="只观察聊天氛围，不抢答",
        roles=["observer"],
    )

    async def on_observe(self, text: str, user_id: str = "", metadata: dict | None = None):
        # 这里可以记录统计信息，但不要回复用户
        return None


Plugin = MoodObserverPlugin
```

## config.json

推荐 schema v2：

```json
{
  "schema_version": 2,
  "id": "example_plugin",
  "name": "example_plugin",
  "cn_name": "示例插件",
  "version": "1.0.0",
  "author": "your-name",
  "description": "一句话说明插件做什么",
  "full_description": "更详细的介绍",
  "category": "实用工具",
  "keywords": ["示例"],
  "triggers": ["示例"],
  "features": ["演示插件结构"],
  "usage": "对白说「示例」即可触发",
  "commands": ["示例"],
  "changelog": "v1.0.0 - 初始版本",
  "notes": "",
  "roles": ["interceptor"],
  "platforms": ["qq", "desktop"],
  "permissions": [],
  "requires_service": [],
  "dependencies": {
    "python": []
  },
  "assets": []
}
```

字段说明：

| 字段 | 说明 |
|------|------|
| `roles` | 插件参与的链路角色 |
| `platforms` | 适用平台，例如 `qq`、`desktop`、`bilibili`、`qzone`、`server`、`all` |
| `permissions` | 需要提示用户的权限，例如 `owner`、`admin`、`network`、`filesystem` |
| `requires_service` | 依赖的外部服务，例如 `napcat`、`comfyui`、`siliconflow` |
| `dependencies` | 额外 Python 依赖声明，只用于展示和安装前提示 |
| `assets` | 需要随插件下载的资源文件路径，必须是插件目录内部相对路径 |

## 资源文件

资源文件必须位于当前插件目录内，例如：

```json
{
  "assets": [
    "assets/icon.png",
    "prompts/system.md",
    "docs/help.md"
  ]
}
```

禁止使用绝对路径或 `..` 路径穿越。

## 提交方式

1. 在线提交：使用 [插件提交页面](https://whitesalary-plugins-web.vercel.app)。
2. Pull Request：把插件目录提交到 `plugins/<plugin_id>/`。
3. 本地同步：在 White Salary 桌面端/控制台里使用插件市场同步功能。

提交后仓库会自动运行脚本生成 `plugins.json`，浏览器市场和桌面端刷新后即可看到。

## 检查清单

- `plugin.py` 能被 Python 正常导入。
- `Plugin = YourPluginClass` 已导出。
- `config.json` 的 `id` 与目录名一致。
- 只声明实际需要的 `roles`。
- 如果使用网络、文件、账号、截图、控制电脑等能力，在 `permissions` 中写清楚。
- 如果需要 NapCat、ComfyUI、本地 TTS、云端 API 等服务，在 `requires_service` 中写清楚。
