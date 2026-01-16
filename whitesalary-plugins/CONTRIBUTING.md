# 🛠️ 插件開發指南

歡迎為白開發插件！本指南將幫助你快速上手。

## 📋 插件結構

每個插件必須包含以下文件：

```
your_plugin/
├── plugin.py      # 主程序文件（必需）
├── config.json    # 插件配置（必需）
└── README.md      # 說明文檔（推薦）
```

## 📝 config.json 格式

```json
{
    "id": "your_plugin_id",
    "name": "插件英文名",
    "cn_name": "插件中文名",
    "version": "1.0.0",
    "author": "你的名字",
    "description": "插件的簡短描述",
    "category": "娱乐",
    "keywords": ["关键词1", "关键词2"],
    "triggers": ["触发词1", "触发词2"],
    "features": [
        "功能特色1",
        "功能特色2"
    ],
    "usage": "使用方法說明",
    "changelog": "v1.0.0 - 初始版本"
}
```

### 可用分類 (category)
- `娱乐` - 遊戲、運勢等娛樂功能
- `工具` - 實用工具類
- `信息` - 資訊查詢類
- `社交` - 社交互動類
- `媒体` - 圖片、音樂、視頻相關
- `自动化` - 自動化任務

## 🐍 plugin.py 模板

```python
"""
插件名稱
描述：這個插件做什麼
作者：你的名字
"""

import re
from typing import Optional, Dict, Any


class Plugin:
    """插件主類"""
    
    def __init__(self):
        self.name = "your_plugin"
        self.cn_name = "插件中文名"
        self.description = "插件描述"
        self.version = "1.0.0"
        self.author = "你的名字"
        
        # 觸發關鍵詞（正則表達式）
        self.triggers = [
            r"关键词1",
            r"关键词2",
        ]
    
    def can_handle(self, message: str) -> bool:
        """檢查是否應該處理這條消息"""
        for trigger in self.triggers:
            if re.search(trigger, message, re.IGNORECASE):
                return True
        return False
    
    async def handle(self, message: str, context: Dict[str, Any]) -> Optional[str]:
        """
        處理消息並返回響應
        
        Args:
            message: 用戶發送的消息
            context: 上下文信息，包含：
                - user_id: 用戶ID
                - group_id: 群組ID（如果是群聊）
                - is_owner: 是否是主人
                - adapter: 適配器實例
        
        Returns:
            響應文本，或 None 表示不響應
        """
        # 在這裡實現你的邏輯
        return "這是插件的回覆！"


# 導出插件實例
plugin = Plugin()
```

## 🔧 進階功能

### 使用配置文件
```python
import json
import os

class Plugin:
    def __init__(self):
        # 加載配置
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
```

### 持久化數據
```python
import json
import os

class Plugin:
    def save_data(self, data: dict):
        """保存數據"""
        data_path = os.path.join(os.path.dirname(__file__), 'data.json')
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_data(self) -> dict:
        """加載數據"""
        data_path = os.path.join(os.path.dirname(__file__), 'data.json')
        if os.path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
```

### 使用外部 API
```python
import aiohttp

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

## 📤 提交插件

### 步驟
1. **Fork** 本倉庫
2. **創建**你的插件文件夾在 `plugins/` 目錄下
3. **確保**包含 `plugin.py` 和 `config.json`
4. **測試**你的插件能正常工作
5. **提交** Pull Request

### PR 標題格式
```
[新插件] 插件中文名 - 簡短描述
```

### 自動審核
提交 PR 後，GitHub Actions 會自動：
1. ✅ 檢查文件結構是否正確
2. ✅ 驗證 config.json 格式
3. ✅ 檢查 plugin.py 語法
4. ✅ 通過後自動合併
5. ✅ 自動更新插件列表

## ❓ 常見問題

### Q: 我的插件可以調用白的其他功能嗎？
A: 可以！通過 `context['adapter']` 可以訪問適配器功能。

### Q: 插件可以定時執行嗎？
A: 目前不支持，但可以通過配合提醒功能實現類似效果。

### Q: 如何調試插件？
A: 在本地的 WhiteSalary `plugins/` 目錄下開發和測試。

---

有問題？歡迎在 Issues 中提出！

