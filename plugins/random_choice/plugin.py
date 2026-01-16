"""随机选择插件 - 帮你做决定"""
import random

def run(options: list = None, **kwargs):
    """随机选择一个选项"""
    if not options or len(options) < 2:
        return "请提供至少两个选项让我帮你选择！\n用法：帮我选 选项1 选项2 选项3"
    
    choice = random.choice(options)
    
    responses = [
        f"🎯 我选择了：**{choice}**！就这个了！",
        f"✨ 命运之轮指向了：**{choice}**！",
        f"🎲 随机结果：**{choice}**！别犹豫了！",
        f"💫 我觉得 **{choice}** 不错！",
        f"🔮 经过深思熟虑...选 **{choice}**！"
    ]
    
    return random.choice(responses)

