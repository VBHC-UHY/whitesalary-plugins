"""快速翻译插件 - 中英互译（简单词典）"""

# 简单的中英词典
DICT_EN_TO_CN = {
    "hello": "你好", "world": "世界", "love": "爱", "happy": "开心",
    "sad": "难过", "good": "好", "bad": "坏", "beautiful": "美丽",
    "cat": "猫", "dog": "狗", "sun": "太阳", "moon": "月亮",
    "water": "水", "fire": "火", "tree": "树", "flower": "花",
    "yes": "是", "no": "否", "thank you": "谢谢", "sorry": "对不起"
}

DICT_CN_TO_EN = {v: k for k, v in DICT_EN_TO_CN.items()}

def is_chinese(text):
    """判断是否包含中文"""
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False

def run(text: str = None, **kwargs):
    """翻译文本"""
    if not text:
        return "请提供要翻译的文本！\n用法：翻译 hello"
    
    text = text.strip().lower()
    
    if is_chinese(text):
        # 中译英
        if text in DICT_CN_TO_EN:
            return f"🌐 **翻译结果**\n\n{text} → **{DICT_CN_TO_EN[text]}**"
        else:
            return f"🌐 抱歉，我的词典里还没有「{text}」的翻译\n（提示：这是简化版翻译，仅支持常用词汇）"
    else:
        # 英译中
        if text in DICT_EN_TO_CN:
            return f"🌐 **翻译结果**\n\n{text} → **{DICT_EN_TO_CN[text]}**"
        else:
            return f"🌐 抱歉，我的词典里还没有「{text}」的翻译\n（提示：这是简化版翻译，仅支持常用词汇）"

