"""摸鱼提醒插件 - 打工人的好帮手"""
from datetime import datetime

WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

def run(**kwargs):
    """生成摸鱼日历"""
    now = datetime.now()
    weekday = now.weekday()  # 0=周一, 6=周日
    
    days_to_weekend = 5 - weekday if weekday < 5 else 0
    days_to_monday = 7 - weekday if weekday > 0 else 0
    
    progress = "🐟" * (weekday + 1) + "⬜" * (6 - weekday)
    
    result = f"""🐟 **摸鱼人日历** 🐟

📅 今天是 **{WEEKDAYS[weekday]}**
📊 本周进度：{progress}

"""
    
    if weekday < 5:
        result += f"⏰ 距离周末还有 **{days_to_weekend}** 天\n"
        result += f"💪 再坚持一下！摸鱼使我快乐！\n"
        
        if weekday == 4:
            result += "\n🎉 **今天周五啦！胜利在望！**"
        elif weekday == 0:
            result += "\n😫 周一综合症...加油打工人！"
    else:
        result += f"🎉 今天是 **周末**！好好休息！\n"
        result += f"😱 距离周一还有 **{days_to_monday}** 天..."
    
    return result

