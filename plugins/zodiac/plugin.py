"""星座运势插件"""
import random
from datetime import datetime

ZODIAC_SIGNS = {
    "白羊座": "♈", "金牛座": "♉", "双子座": "♊", "巨蟹座": "♋",
    "狮子座": "♌", "处女座": "♍", "天秤座": "♎", "天蝎座": "♏",
    "射手座": "♐", "摩羯座": "♑", "水瓶座": "♒", "双鱼座": "♓"
}

def get_fortune():
    """生成随机运势"""
    return random.randint(60, 100)

def run(sign: str = None, **kwargs):
    """查询星座运势"""
    if not sign:
        signs = ", ".join(ZODIAC_SIGNS.keys())
        return f"请告诉我你的星座！\n\n可选星座：{signs}"
    
    # 标准化星座名称
    if not sign.endswith("座"):
        sign = sign + "座"
    
    if sign not in ZODIAC_SIGNS:
        return f"⚠️ 未知星座：{sign}\n\n可选星座：{', '.join(ZODIAC_SIGNS.keys())}"
    
    # 生成运势
    today = datetime.now().strftime("%Y-%m-%d")
    emoji = ZODIAC_SIGNS[sign]
    
    overall = get_fortune()
    love = get_fortune()
    career = get_fortune()
    wealth = get_fortune()
    
    # 生成幸运物
    lucky_colors = ["红色", "蓝色", "绿色", "紫色", "金色", "白色", "粉色"]
    lucky_numbers = list(range(1, 10))
    
    result = f"""
{emoji} **{sign}今日运势** {emoji}

📅 日期：{today}

⭐ **综合运势**：{'★' * (overall // 20)}{'☆' * (5 - overall // 20)} {overall}分
💕 **爱情运势**：{'★' * (love // 20)}{'☆' * (5 - love // 20)} {love}分
💼 **事业运势**：{'★' * (career // 20)}{'☆' * (5 - career // 20)} {career}分
💰 **财富运势**：{'★' * (wealth // 20)}{'☆' * (5 - wealth // 20)} {wealth}分

🎨 幸运颜色：{random.choice(lucky_colors)}
🔢 幸运数字：{random.choice(lucky_numbers)}

💡 今日提醒：{"今天运势不错，适合开展新计划！" if overall >= 80 else "稳扎稳打，不宜冒险。"}
"""
    
    return result.strip()

