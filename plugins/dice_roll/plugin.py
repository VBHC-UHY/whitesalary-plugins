"""
骰子插件
描述：支持多种骰子的投掷功能
作者：WhiteSalary
"""

import re
import random
from typing import Optional, Dict, Any, List, Tuple


class Plugin:
    """骰子插件"""
    
    def __init__(self):
        self.name = "dice_roll"
        self.cn_name = "骰子"
        self.description = "支持多种骰子的投掷功能"
        self.version = "1.0.0"
        self.author = "WhiteSalary"
        
        # 触发关键词
        self.triggers = [
            r"掷骰子",
            r"投骰子",
            r"扔骰子",
            r"roll",
            r"\d+d\d+",  # 如 1d6, 2d20
            r"\d+个.*骰",
        ]
        
        # 骰子面数映射
        self.dice_names = {
            4: "四面骰",
            6: "六面骰",
            8: "八面骰",
            10: "十面骰",
            12: "十二面骰",
            20: "二十面骰",
            100: "百面骰",
        }
    
    def can_handle(self, message: str) -> bool:
        """检查是否应该处理这条消息"""
        for trigger in self.triggers:
            if re.search(trigger, message, re.IGNORECASE):
                return True
        return False
    
    def _parse_dice_notation(self, message: str) -> Tuple[int, int]:
        """解析骰子表示法（如 2d6 表示 2 个 6 面骰）"""
        # 标准 NdM 格式
        match = re.search(r"(\d+)d(\d+)", message, re.IGNORECASE)
        if match:
            count = int(match.group(1))
            sides = int(match.group(2))
            return min(count, 100), max(2, min(sides, 1000))  # 限制范围
        
        # 中文格式：3个六面骰
        match = re.search(r"(\d+)\s*个.*?(\d+)\s*面", message)
        if match:
            count = int(match.group(1))
            sides = int(match.group(2))
            return min(count, 100), max(2, min(sides, 1000))
        
        # 简单格式：掷骰子
        if re.search(r"骰子|roll", message, re.IGNORECASE):
            return 1, 6  # 默认 1d6
        
        return 1, 6
    
    def _roll_dice(self, count: int, sides: int) -> List[int]:
        """投掷骰子"""
        return [random.randint(1, sides) for _ in range(count)]
    
    def _format_results(self, results: List[int], sides: int) -> str:
        """格式化结果"""
        dice_name = self.dice_names.get(sides, f"{sides}面骰")
        count = len(results)
        total = sum(results)
        
        # 骰子表情
        dice_emojis = {
            1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"
        }
        
        # 构建结果显示
        if count == 1:
            result_str = str(results[0])
            if sides == 6 and results[0] in dice_emojis:
                result_str = f"{dice_emojis[results[0]]} {results[0]}"
        else:
            if sides == 6:
                result_str = " + ".join(
                    f"{dice_emojis.get(r, '')} {r}" if r <= 6 else str(r) 
                    for r in results
                )
            else:
                result_str = " + ".join(map(str, results))
        
        # 构建响应
        response = f"🎲 投掷 {count} 个{dice_name}\n\n"
        response += f"结果：{result_str}\n"
        
        if count > 1:
            response += f"总和：{total}\n"
            response += f"平均：{total/count:.1f}\n"
            response += f"最大：{max(results)} | 最小：{min(results)}"
        
        # 特殊结果
        if count == 1:
            if results[0] == sides:
                response += "\n\n🎉 大成功！满点！"
            elif results[0] == 1:
                response += "\n\n😅 大失败...最小点"
        
        return response
    
    async def handle(self, message: str, context: Dict[str, Any]) -> Optional[str]:
        """处理消息并返回骰子结果"""
        # 解析骰子参数
        count, sides = self._parse_dice_notation(message)
        
        # 投掷骰子
        results = self._roll_dice(count, sides)
        
        # 格式化并返回结果
        return self._format_results(results, sides)


# 导出插件实例
plugin = Plugin()


