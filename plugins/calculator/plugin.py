"""计算器插件 - 数学运算"""
import math
import re

def run(expression: str = None, **kwargs):
    """计算数学表达式"""
    if not expression:
        return "请提供要计算的表达式！\n用法：计算 (1+2)*3"
    
    # 安全检查：只允许数字和基本运算符
    safe_pattern = r'^[\d\s\+\-\*\/\(\)\.\%\^]+$'
    
    # 替换一些常见写法
    expr = expression.replace('×', '*').replace('÷', '/').replace('^', '**').replace('x', '*')
    
    if not re.match(safe_pattern, expr):
        return "⚠️ 表达式包含不支持的字符\n支持：数字、+ - * / ( ) % ^"
    
    try:
        # 计算结果
        result = eval(expr)
        
        # 格式化输出
        if isinstance(result, float):
            if result == int(result):
                result = int(result)
            else:
                result = round(result, 6)
        
        return f"🔢 **计算结果**\n\n{expression} = **{result}**"
        
    except ZeroDivisionError:
        return "⚠️ 错误：除数不能为零！"
    except Exception as e:
        return f"⚠️ 计算错误：表达式格式不正确"

