# 测试插件
class TestPlugin:
    name = "test_plugin"
    cn_name = "测试插件"
    
    async def execute(self, message):
        return "测试成功！"
