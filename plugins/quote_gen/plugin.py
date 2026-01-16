"""名言生成插件"""
import random

QUOTES = {
    "励志": [
        "成功不是终点，失败也并非致命，重要的是继续前进的勇气。—— 丘吉尔",
        "生活就像骑自行车，要保持平衡就得不断前进。—— 爱因斯坦",
        "不要等待机会，而要创造机会。",
        "每一个不曾起舞的日子，都是对生命的辜负。—— 尼采",
        "你的时间有限，不要浪费在别人的生活里。—— 乔布斯"
    ],
    "毒鸡汤": [
        "努力不一定成功，但不努力真的很舒服。",
        "只要你足够努力，没有什么事是搞不砸的。",
        "丑小鸭能变成白天鹅，不是因为它努力，是因为它爸妈本来就是白天鹅。",
        "条条大路通罗马，但有人就出生在罗马。",
        "失败是成功之母，成功他爸不详。",
        "比你优秀的人还在努力，你努力还有什么用？"
    ],
    "名人名言": [
        "知之为知之，不知为不知，是知也。—— 孔子",
        "天行健，君子以自强不息。—— 《周易》",
        "学而不思则罔，思而不学则殆。—— 孔子",
        "三人行，必有我师焉。—— 孔子",
        "己所不欲，勿施于人。—— 孔子"
    ]
}

def run(quote_type: str = None, **kwargs):
    """生成名言"""
    if quote_type and quote_type in QUOTES:
        quote = random.choice(QUOTES[quote_type])
        return f"📜 【{quote_type}】\n\n{quote}"
    else:
        quote_type = random.choice(list(QUOTES.keys()))
        quote = random.choice(QUOTES[quote_type])
        return f"📜 【{quote_type}】\n\n{quote}\n\n💡 可选类型：{', '.join(QUOTES.keys())}"

