#!/usr/bin/env python3
"""
Generate plugins.json and README.md for the White Salary plugin market.

The index is schema v2, but remains backward compatible with older plugin
configs that do not declare roles/platforms/assets/dependencies.
"""

import json
import os
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any


ROOT_DIR = Path(__file__).parent.parent
PLUGINS_DIR = ROOT_DIR / "plugins"
OUTPUT_FILE = ROOT_DIR / "plugins.json"
README_FILE = ROOT_DIR / "README.md"

GITHUB_USER = os.environ.get("GITHUB_REPOSITORY_OWNER", "VBHC-UHY")
GITHUB_REPO = "whitesalary-plugins"
MARKET_SCHEMA_VERSION = 2
DEFAULT_ROLES = ["interceptor", "rewriter", "tool_provider"]
DEFAULT_PLATFORMS = ["all"]
VALID_ROLES = {"interceptor", "rewriter", "tool_provider", "observer"}
ROLE_ALIASES = {
    "message": "interceptor",
    "reply": "rewriter",
    "tool": "tool_provider",
    "tools": "tool_provider",
    "observe": "observer",
}
ROLE_LABELS = {
    "interceptor": "抢答/拦截",
    "rewriter": "改写回复",
    "tool_provider": "提供工具",
    "observer": "只观察学习",
}


def as_list(value: Any) -> list[Any]:
    if value is None or value == "":
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.replace("，", ",").split(",") if item.strip()]
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [value]


def normalize_string_list(
    value: Any,
    *,
    default: list[str] | tuple[str, ...] = (),
    aliases: dict[str, str] | None = None,
    allowed: set[str] | None = None,
) -> list[str]:
    raw_items = as_list(value)
    if not raw_items:
        return list(default)

    result: list[str] = []
    for raw in raw_items:
        item = str(raw).strip().lower()
        if not item:
            continue
        item = (aliases or {}).get(item, item)
        if allowed is not None and item not in allowed:
            print(f"    WARN skip unsupported value: {item}")
            continue
        if item not in result:
            result.append(item)
    return result or list(default)


def normalize_asset_paths(value: Any) -> list[str]:
    result: list[str] = []
    for raw in as_list(value):
        rel = str(raw).strip().replace("\\", "/").lstrip("/")
        if not rel:
            continue
        posix = PurePosixPath(rel)
        if posix.is_absolute() or ".." in posix.parts:
            print(f"    WARN skip unsafe asset path: {raw}")
            continue
        if rel in {"plugin.py", "config.json", "__init__.py"}:
            continue
        if rel not in result:
            result.append(rel)
    return result


def normalize_dependencies(value: Any) -> dict[str, Any]:
    if value in (None, ""):
        return {}
    if isinstance(value, dict):
        return value
    python = [str(item).strip() for item in as_list(value) if str(item).strip()]
    return {"python": python} if python else {}


def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_plugin_config(plugin_dir: Path) -> dict | None:
    return load_json(plugin_dir / "config.json")


def load_existing_index() -> dict[str, dict]:
    existing = load_json(OUTPUT_FILE)
    if not existing:
        return {}
    plugins = existing if isinstance(existing, list) else existing.get("plugins", [])
    return {plugin.get("id"): plugin for plugin in plugins if isinstance(plugin, dict) and plugin.get("id")}


def generate_download_url(plugin_id: str) -> str:
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/plugins/{plugin_id}"


def build_plugin_info(plugin_dir: Path, config: dict, old_entry: dict | None = None) -> dict:
    old_entry = old_entry or {}
    plugin_id = config.get("id", plugin_dir.name)
    return {
        "schema_version": MARKET_SCHEMA_VERSION,
        "id": plugin_id,
        "name": config.get("name", plugin_id),
        "cn_name": config.get("cn_name", config.get("name", plugin_id)),
        "version": config.get("version", "1.0.0"),
        "author": config.get("author", "anonymous"),
        "description": config.get("description", ""),
        "full_description": config.get("full_description", config.get("description", "")),
        "category": config.get("category", "工具"),
        "keywords": as_list(config.get("keywords", [])),
        "triggers": as_list(config.get("triggers", [])),
        "features": as_list(config.get("features", [])),
        "usage": config.get("usage", ""),
        "commands": as_list(config.get("commands", config.get("triggers", []))),
        "changelog": config.get("changelog", ""),
        "notes": config.get("notes", ""),
        "roles": normalize_string_list(
            config.get("roles"),
            default=DEFAULT_ROLES,
            aliases=ROLE_ALIASES,
            allowed=VALID_ROLES,
        ),
        "platforms": normalize_string_list(config.get("platforms"), default=DEFAULT_PLATFORMS),
        "permissions": normalize_string_list(config.get("permissions", [])),
        "requires_service": normalize_string_list(
            config.get("requires_service", config.get("requires_services", []))
        ),
        "dependencies": normalize_dependencies(config.get("dependencies", {})),
        "assets": normalize_asset_paths(config.get("assets", [])),
        "downloads": int(config.get("downloads", old_entry.get("downloads", 0)) or 0),
        "rating": float(config.get("rating", old_entry.get("rating", 5.0)) or 5.0),
        "featured": bool(config.get("featured", old_entry.get("featured", False))),
        "download_url": generate_download_url(plugin_id),
    }


def main() -> None:
    plugins: list[dict] = []
    existing_index = load_existing_index()

    print(f"Scanning plugin dir: {PLUGINS_DIR}")

    for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
        if not plugin_dir.is_dir() or plugin_dir.name.startswith("."):
            continue

        print(f"  Processing plugin: {plugin_dir.name}")
        config = load_plugin_config(plugin_dir)
        if not config:
            print("    WARN skip: missing config.json")
            continue

        required_fields = ["id", "cn_name", "version", "author", "description"]
        missing = [field for field in required_fields if field not in config]
        if missing:
            print(f"    WARN skip: missing fields {missing}")
            continue

        plugin_info = build_plugin_info(
            plugin_dir,
            config,
            existing_index.get(config.get("id", plugin_dir.name)),
        )
        plugins.append(plugin_info)
        print("    OK added")

    plugins.sort(key=lambda item: item["cn_name"])

    output = {
        "version": "2.0.0",
        "schema_version": MARKET_SCHEMA_VERSION,
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "total_count": len(plugins),
        "plugins": plugins,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("\nOK generated plugins.json")
    print(f"   Total plugins: {len(plugins)}")

    generate_readme(plugins)
    print("OK updated README.md")


def escape_table(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def summarize_roles(roles: list[str]) -> str:
    return " / ".join(ROLE_LABELS.get(role, role) for role in roles)


def generate_readme(plugins: list[dict]) -> None:
    categories: dict[str, list[dict]] = {}
    for plugin in plugins:
        categories.setdefault(plugin.get("category", "其他"), []).append(plugin)

    rows = []
    for plugin in plugins:
        emoji = get_category_emoji(plugin.get("category", "其他"))
        rows.append(
            "| "
            + " | ".join(
                [
                    f"{emoji} {escape_table(plugin['cn_name'])}",
                    escape_table(plugin["description"][:40] + ("..." if len(plugin["description"]) > 40 else "")),
                    escape_table(summarize_roles(plugin.get("roles", DEFAULT_ROLES))),
                    escape_table(", ".join(plugin.get("platforms", DEFAULT_PLATFORMS))),
                    escape_table(plugin["version"]),
                    escape_table(plugin["author"]),
                    escape_table(plugin.get("category", "其他")),
                ]
            )
            + " |"
        )

    category_lines = []
    for category, category_plugins in sorted(categories.items()):
        category_lines.append(f"- {get_category_emoji(category)} **{category}**: {len(category_plugins)} 个插件")

    readme = f"""# 🏠 WhiteSalary 插件市场

![插件数量](https://img.shields.io/badge/插件数量-{len(plugins)}-blue)
![市场索引](https://img.shields.io/badge/schema-v2-green)
![许可证](https://img.shields.io/badge/license-MIT-yellow)

这是 White Salary 的公开插件仓库。桌面端插件市场、浏览器展示市场和浏览器提交市场都会读取这里的数据。

## 🍃 可用插件

| 插件名称 | 描述 | 角色 | 平台 | 版本 | 作者 | 分类 |
|---------|------|------|------|------|------|------|
{chr(10).join(rows)}

## 📦 分类统计

{chr(10).join(category_lines)}

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
{{
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
  "dependencies": {{
    "python": ["httpx"]
  }},
  "assets": ["assets/icon.png"]
}}
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

*最后更新：{datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""

    with open(README_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(readme)


def get_category_emoji(category: str) -> str:
    emoji_map = {
        "娱乐": "🎮",
        "娱乐游戏": "🎮",
        "信息": "📰",
        "新闻资讯": "📰",
        "工具": "🔧",
        "实用工具": "🔧",
        "社交": "💬",
        "社交互动": "💬",
        "AI": "🤖",
        "AI增强": "🤖",
        "音乐": "🎵",
        "音乐音频": "🎵",
        "图片": "🖼️",
        "图片处理": "🖼️",
        "视频": "🎬",
        "视频相关": "🎬",
        "媒体": "📺",
        "媒体综合": "📺",
        "天气": "☀️",
        "天气日历": "☀️",
        "搜索": "🔍",
        "网络搜索": "🔍",
        "翻译": "🌐",
        "翻译语言": "🌐",
        "自动化": "⚡",
        "提醒": "⏰",
        "提醒待办": "⏰",
        "数据": "📊",
        "数据处理": "📊",
        "开发": "💻",
        "开发工具": "💻",
        "生活": "🏠",
        "生活服务": "🏠",
        "学习": "📚",
        "学习教育": "📚",
        "金融": "💰",
        "财务金融": "💰",
        "健康": "❤️",
        "健康运动": "❤️",
        "群管理": "👮",
        "群互动": "🎉",
        "系统管理": "⚙️",
        "其他": "📦",
    }
    return emoji_map.get(category, "📦")


if __name__ == "__main__":
    main()
