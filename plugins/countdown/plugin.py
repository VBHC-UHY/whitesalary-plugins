"""倒数计时插件 - 计算距离目标日期的天数"""
from datetime import datetime, date

def run(target_date: str = None, event_name: str = "目标日期", **kwargs):
    """计算距离目标日期还有多少天"""
    if not target_date:
        return "请告诉我目标日期！\n用法：距离2026-12-31还有几天"
    
    try:
        # 尝试解析日期
        if "-" in target_date:
            target = datetime.strptime(target_date, "%Y-%m-%d").date()
        elif "/" in target_date:
            target = datetime.strptime(target_date, "%Y/%m/%d").date()
        else:
            return "日期格式不正确，请使用 YYYY-MM-DD 格式"
        
        today = date.today()
        delta = (target - today).days
        
        if delta > 0:
            return f"📅 距离 **{event_name}** 还有 **{delta}** 天！\n⏰ 目标日期：{target_date}"
        elif delta == 0:
            return f"🎉 今天就是 **{event_name}**！"
        else:
            return f"📅 **{event_name}** 已经过去了 **{abs(delta)}** 天"
            
    except ValueError:
        return "日期格式不正确，请使用 YYYY-MM-DD 格式"

