#!/usr/bin/env python3
"""
自动生成 plugins.json 和更新 README.md
扫描 plugins/ 目录下的所有插件，合并到一个 JSON 文件，并更新 README
"""

import os
import json
from datetime import datetime
from pathlib import Path

# 获取项目根目录
ROOT_DIR = Path(__file__).parent.parent
PLUGINS_DIR = ROOT_DIR / 'plugins'
OUTPUT_FILE = ROOT_DIR / 'plugins.json'
README_FILE = ROOT_DIR / 'README.md'

# GitHub 仓库信息（需要替换为实际值）
GITHUB_USER = os.environ.get('GITHUB_REPOSITORY_OWNER', 'VBHC-UHY')
GITHUB_REPO = 'whitesalary-plugins'


def load_plugin_config(plugin_dir: Path) -> dict:
    """加载插件的 config.json"""
    config_path = plugin_dir / 'config.json'
    if not config_path.exists():
        return None
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_download_url(plugin_id: str) -> str:
    """生成插件下载 URL"""
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/plugins/{plugin_id}"


def main():
    plugins = []
    
    print(f"📂 扫描插件目录: {PLUGINS_DIR}")
    
    # 扫描所有插件目录
    for plugin_dir in PLUGINS_DIR.iterdir():
        if not plugin_dir.is_dir():
            continue
        
        # 跳过隐藏目录
        if plugin_dir.name.startswith('.'):
            continue
        
        print(f"  📦 处理插件: {plugin_dir.name}")
        
        # 加载配置
        config = load_plugin_config(plugin_dir)
        if not config:
            print(f"    ⚠️ 跳过: 无 config.json")
            continue
        
        # 确保必需字段存在
        required_fields = ['id', 'cn_name', 'version', 'author', 'description']
        missing = [f for f in required_fields if f not in config]
        if missing:
            print(f"    ⚠️ 跳过: 缺少字段 {missing}")
            continue
        
        # 构建插件信息
        plugin_info = {
            'id': config.get('id', plugin_dir.name),
            'name': config.get('name', config.get('id', plugin_dir.name)),
            'cn_name': config['cn_name'],
            'version': config['version'],
            'author': config['author'],
            'description': config['description'],
            'full_description': config.get('full_description', config['description']),
            'category': config.get('category', '工具'),
            'keywords': config.get('keywords', []),
            'triggers': config.get('triggers', []),
            'features': config.get('features', []),
            'usage': config.get('usage', ''),
            'commands': config.get('commands', config.get('triggers', [])),
            'changelog': config.get('changelog', ''),
            'notes': config.get('notes', ''),
            'downloads': config.get('downloads', 0),
            'rating': config.get('rating', 5.0),
            'featured': config.get('featured', False),
            'download_url': generate_download_url(config.get('id', plugin_dir.name))
        }
        
        plugins.append(plugin_info)
        print(f"    ✅ 已添加")
    
    # 按名称排序
    plugins.sort(key=lambda x: x['cn_name'])
    
    # 生成输出
    output = {
        'version': '1.0.0',
        'last_updated': datetime.now().strftime('%Y-%m-%d'),
        'total_count': len(plugins),
        'plugins': plugins
    }
    
    # 写入文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 已生成 plugins.json")
    print(f"   📊 共 {len(plugins)} 个插件")
    
    # 生成 README.md
    generate_readme(plugins)
    print(f"✅ 已更新 README.md")


def generate_readme(plugins: list):
    """生成 README.md 文件"""
    
    # 按分类统计
    categories = {}
    for p in plugins:
        cat = p.get('category', '其他')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(p)
    
    readme = f'''# 🏪 WhiteSalary 插件市場

![插件數量](https://img.shields.io/badge/插件數量-{len(plugins)}-blue)
![版本](https://img.shields.io/badge/版本-1.0.0-green)
![許可證](https://img.shields.io/badge/許可證-MIT-yellow)

專為 白 (WhiteSalary) 打造的官方插件倉庫。在這裡你可以找到各種擴展白功能的插件，也可以分享你自己開發的插件。

## 🍰 可用插件

| 插件名稱 | 描述 | 版本 | 作者 | 分類 |
|---------|------|------|------|------|
'''
    
    for p in plugins:
        emoji = get_category_emoji(p.get('category', '其他'))
        readme += f"| {emoji} {p['cn_name']} | {p['description'][:30]}... | {p['version']} | {p['author']} | {p.get('category', '其他')} |\n"
    
    readme += f'''
## 📦 分類統計

'''
    for cat, cat_plugins in sorted(categories.items()):
        emoji = get_category_emoji(cat)
        readme += f"- {emoji} **{cat}**: {len(cat_plugins)} 個插件\n"
    
    readme += '''
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

## 📤 提交插件

1. **在線提交**：訪問 [插件提交頁面](https://whitesalary-plugins-web.vercel.app)
2. **本地提交**：在 WhiteSalary WebUI 的「插件市場」頁面點擊「本地提交」

## 📜 許可證

MIT License - 詳見 [LICENSE](LICENSE)

---

*最後更新：''' + datetime.now().strftime('%Y-%m-%d %H:%M') + '''*
'''
    
    with open(README_FILE, 'w', encoding='utf-8') as f:
        f.write(readme)


def get_category_emoji(category: str) -> str:
    """获取分类对应的 emoji"""
    emoji_map = {
        '娱乐': '🎮',
        '娛樂': '🎮',
        '娱乐游戏': '🎮',
        '信息': '📰',
        '資訊': '📰',
        '新闻资讯': '📰',
        '工具': '🔧',
        '实用工具': '🔧',
        '社交': '💬',
        '社交互动': '💬',
        'AI': '🤖',
        'AI增强': '🤖',
        '音乐': '🎵',
        '音乐音频': '🎵',
        '图片': '🖼️',
        '图片处理': '🖼️',
        '视频': '🎬',
        '视频相关': '🎬',
        '媒体': '📺',
        '媒体综合': '📺',
        '天气': '☀️',
        '天气日历': '☀️',
        '搜索': '🔍',
        '网络搜索': '🔍',
        '翻译': '🌐',
        '翻译语言': '🌐',
        '自动化': '⚡',
        '提醒': '⏰',
        '提醒待办': '⏰',
        '数据': '📊',
        '数据分析': '📊',
        '开发': '💻',
        '开发编程': '💻',
        '生活': '🏠',
        '生活服务': '🏠',
        '学习': '📚',
        '学习教育': '📚',
        '金融': '💰',
        '金融理财': '💰',
        '健康': '❤️',
        '健康运动': '❤️',
        '安全': '🔒',
        '安全隐私': '🔒',
        '系统': '⚙️',
        '系统管理': '⚙️',
    }
    return emoji_map.get(category, '📦')


if __name__ == '__main__':
    main()

