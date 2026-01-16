"""
天气查询插件
描述：查询全国各地实时天气信息
作者：WhiteSalary
"""

import re
from typing import Optional, Dict, Any

try:
    import aiohttp
    HAS_AIOHTTP = True
except ImportError:
    HAS_AIOHTTP = False


class Plugin:
    """天气查询插件"""
    
    def __init__(self):
        self.name = "weather"
        self.cn_name = "天气查询"
        self.description = "查询全国各地实时天气信息"
        self.version = "1.0.0"
        self.author = "WhiteSalary"
        
        # 触发关键词
        self.triggers = [
            r"(.+?)天气",
            r"天气(.+)",
            r"查.*天气",
            r"(.+?)气温",
        ]
        
        # 天气 API (使用免费的 wttr.in)
        self.api_url = "https://wttr.in/{city}?format=j1&lang=zh"
    
    def can_handle(self, message: str) -> bool:
        """检查是否应该处理这条消息"""
        for trigger in self.triggers:
            if re.search(trigger, message, re.IGNORECASE):
                return True
        return False
    
    def _extract_city(self, message: str) -> Optional[str]:
        """从消息中提取城市名"""
        # 常见模式
        patterns = [
            r"(.+?)(?:的)?天气",
            r"天气(.+)",
            r"查(.+?)天气",
            r"(.+?)气温",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                city = match.group(1).strip()
                # 过滤掉一些无效词
                if city and city not in ['查', '看', '一下', '帮我', '的']:
                    return city
        
        return None
    
    def _get_weather_emoji(self, condition: str) -> str:
        """根据天气状况返回表情"""
        condition = condition.lower()
        if '晴' in condition:
            return '☀️'
        elif '云' in condition or '阴' in condition:
            return '☁️'
        elif '雨' in condition:
            return '🌧️'
        elif '雪' in condition:
            return '❄️'
        elif '雾' in condition or '霾' in condition:
            return '🌫️'
        elif '风' in condition:
            return '💨'
        else:
            return '🌤️'
    
    async def _fetch_weather(self, city: str) -> Optional[dict]:
        """获取天气数据"""
        if not HAS_AIOHTTP:
            return None
        
        try:
            async with aiohttp.ClientSession() as session:
                url = self.api_url.format(city=city)
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        return await response.json()
        except Exception as e:
            print(f"天气查询失败: {e}")
        
        return None
    
    async def handle(self, message: str, context: Dict[str, Any]) -> Optional[str]:
        """处理消息并返回天气信息"""
        # 提取城市
        city = self._extract_city(message)
        if not city:
            return "请告诉我你想查询哪个城市的天气哦～\n例如：北京天气"
        
        # 如果没有 aiohttp，返回模拟数据
        if not HAS_AIOHTTP:
            return self._generate_mock_weather(city)
        
        # 获取天气数据
        data = await self._fetch_weather(city)
        
        if not data:
            return f"抱歉，暂时无法获取 {city} 的天气信息 😢"
        
        try:
            # 解析数据
            current = data['current_condition'][0]
            location = data['nearest_area'][0]
            
            city_name = location.get('areaName', [{}])[0].get('value', city)
            temp = current.get('temp_C', 'N/A')
            feels_like = current.get('FeelsLikeC', temp)
            humidity = current.get('humidity', 'N/A')
            condition = current.get('lang_zh', [{}])[0].get('value', current.get('weatherDesc', [{}])[0].get('value', '未知'))
            wind_speed = current.get('windspeedKmph', 'N/A')
            
            emoji = self._get_weather_emoji(condition)
            
            response = f"""🌍 {city_name} 天气

{emoji} 天气状况：{condition}
🌡️ 当前温度：{temp}°C
🤔 体感温度：{feels_like}°C
💧 相对湿度：{humidity}%
💨 风速：{wind_speed} km/h

祝你今天愉快！"""
            
            return response
            
        except Exception as e:
            return f"天气数据解析失败，请稍后再试 😅"
    
    def _generate_mock_weather(self, city: str) -> str:
        """生成模拟天气数据（当没有 aiohttp 时使用）"""
        import random
        
        conditions = ['晴朗', '多云', '小雨', '阴天']
        condition = random.choice(conditions)
        temp = random.randint(5, 30)
        humidity = random.randint(30, 90)
        
        emoji = self._get_weather_emoji(condition)
        
        return f"""🌍 {city} 天气

{emoji} 天气状况：{condition}
🌡️ 当前温度：{temp}°C
💧 相对湿度：{humidity}%

（注：这是模拟数据，请安装 aiohttp 获取实时天气）"""


# 导出插件实例
plugin = Plugin()

