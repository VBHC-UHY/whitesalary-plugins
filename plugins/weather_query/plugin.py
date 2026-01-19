# -*- coding: utf-8 -*-
"""
天气查询插件
当用户询问天气时，返回模拟的天气信息
"""
import logging
import random
from typing import Optional
from src.core.plugins.base import BasePlugin, PluginMeta

logger = logging.getLogger(__name__)


class WeatherQueryPlugin(BasePlugin):
    """天气查询插件"""
    
    meta = PluginMeta(
        name="weather_query",
        version="1.0.0",
        author="WhiteSalary",
        description="查询天气信息，支持关键词触发"
    )
    
    # 触发关键词
    TRIGGERS = ["天气", "气温", "下雨", "晴天", "温度", "多少度"]
    
    # 模拟天气数据
    WEATHER_DATA = {
        "晴": ["阳光明媚，适合出门散步~", "今天天气超好！", "蓝天白云，心情也变好了呢"],
        "多云": ["云朵飘飘的一天", "不冷不热刚刚好", "天阴阴的，但不会下雨"],
        "雨": ["记得带伞哦~", "雨天适合宅在家", "淅淅沥沥的小雨，很有诗意呢"],
        "雪": ["下雪啦！好想堆雪人", "注意保暖哦~", "银装素裹的世界"]
    }
    
    async def on_load(self) -> None:
        """插件加载"""
        self.log(f"✅ {self.meta.name} v{self.meta.version} 已加载")
    
    async def on_message(self, message: str, user_id: str, group_id: Optional[str] = None, **kwargs) -> Optional[str]:
        """处理消息"""
        # 检查是否触发
        if not any(trigger in message for trigger in self.TRIGGERS):
            return None
        
        # 模拟天气
        weather = random.choice(list(self.WEATHER_DATA.keys()))
        temp = random.randint(15, 30)
        desc = random.choice(self.WEATHER_DATA[weather])
        
        return f"现在天气{weather}，气温{temp}℃~\n{desc}"


Plugin = WeatherQueryPlugin