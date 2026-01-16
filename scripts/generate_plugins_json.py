#!/usr/bin/env python3
"""
自动生成 plugins.json
扫描 plugins/ 目录下的所有插件，合并到一个 JSON 文件
"""

import os
import json
from datetime import datetime
from pathlib import Path

# 获取项目根目录
ROOT_DIR = Path(__file__).parent.parent
PLUGINS_DIR = ROOT_DIR / 'plugins'
OUTPUT_FILE = ROOT_DIR / 'plugins.json'

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


if __name__ == '__main__':
    main()

