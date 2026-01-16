"""
每日运势插件
描述：为用户生成每日专属运势预测
作者：WhiteSalary
"""

import re
import random
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any


class Plugin:
    """每日运势插件"""
    
    def __init__(self):
        self.name = "daily_fortune"
        self.cn_name = "每日运势"
        self.description = "每天为用户生成专属运势预测"
        self.version = "1.0.0"
        self.author = "WhiteSalary"
        
        # 触发关键词
        self.triggers = [
            r"今日运势",
            r"运势",
            r"算卦",
            r"今天运气",
            r"看看.*运气",
            r"帮我算",
        ]
        
        # 运势等级
        self.fortune_levels = [
            ("大吉", "🌟", "今天是你的幸运日！"),
            ("吉", "✨", "今天运气不错哦～"),
            ("中吉", "🌸", "平稳的一天，保持好心情"),
            ("小吉", "🍀", "小小的好运在等着你"),
            ("末吉", "🌿", "今天适合静心沉淀"),
            ("凶", "🌧️", "今天要小心行事"),
        ]
        
        # 幸运颜色
        self.lucky_colors = ["红色", "蓝色", "绿色", "紫色", "金色", "粉色", "白色", "橙色"]
        
        # 幸运方向
        self.lucky_directions = ["东", "南", "西", "北", "东南", "东北", "西南", "西北"]
    
    def can_handle(self, message: str) -> bool:
        """检查是否应该处理这条消息"""
        for trigger in self.triggers:
            if re.search(trigger, message, re.IGNORECASE):
                return True
        return False
    
    def _generate_seed(self, user_id: str) -> int:
        """根据用户ID和日期生成随机种子"""
        today = datetime.now().strftime("%Y-%m-%d")
        seed_str = f"{user_id}_{today}"
        return int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)
    
    def _get_fortune(self, seed: int) -> tuple:
        """获取运势"""
        random.seed(seed)
        return random.choice(self.fortune_levels)
    
    def _get_lucky_number(self, seed: int) -> int:
        """获取幸运数字"""
        random.seed(seed + 1)
        return random.randint(1, 99)
    
    def _get_lucky_color(self, seed: int) -> str:
        """获取幸运颜色"""
        random.seed(seed + 2)
        return random.choice(self.lucky_colors)
    
    def _get_lucky_direction(self, seed: int) -> str:
        """获取幸运方向"""
        random.seed(seed + 3)
        return random.choice(self.lucky_directions)
    
    def _get_aspect_fortune(self, seed: int, aspect: str) -> str:
        """获取各方面运势"""
        random.seed(seed + hash(aspect))
        stars = random.randint(1, 5)
        return "⭐" * stars + "☆" * (5 - stars)
    
    async def handle(self, message: str, context: Dict[str, Any]) -> Optional[str]:
        """处理消息并返回运势"""
        user_id = str(context.get('user_id', 'default'))
        
        # 生成随机种子
        seed = self._generate_seed(user_id)
        
        # 获取各项运势
        fortune_level, emoji, fortune_desc = self._get_fortune(seed)
        lucky_number = self._get_lucky_number(seed)
        lucky_color = self._get_lucky_color(seed)
        lucky_direction = self._get_lucky_direction(seed)
        
        # 各方面运势
        love_fortune = self._get_aspect_fortune(seed, "love")
        money_fortune = self._get_aspect_fortune(seed, "money")
        work_fortune = self._get_aspect_fortune(seed, "work")
        health_fortune = self._get_aspect_fortune(seed, "health")
        
        # 构建响应
        today = datetime.now().strftime("%Y年%m月%d日")
        
        response = f"""🔮 {today} 运势

{emoji} 今日运势：【{fortune_level}】
{fortune_desc}

📊 详细运势：
  💕 爱情：{love_fortune}
  💰 财运：{money_fortune}
  💼 事业：{work_fortune}
  💪 健康：{health_fortune}

🎯 幸运指南：
  🔢 幸运数字：{lucky_number}
  🎨 幸运颜色：{lucky_color}
  🧭 幸运方位：{lucky_direction}

✨ 祝你今天好运！"""
        
        return response


# 导出插件实例
plugin = Plugin()



