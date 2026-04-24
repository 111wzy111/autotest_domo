# autotest_domo
基于 Python + requests 的接口自动化测试示例，项目采取分层设计：api层、用例层，通过配置文件管理测试环境数据；包含 token 获取、标签查询、标签停用/启用、异常场景，以及给人打标签、移除标签的端到端场景。

- 核心接口增加超时判断及重试机制，并通过 Charles 模拟弱网验证。
- 测试数据与代码分离，异常场景通过 JSON 文件 + @pytest.mark.parametrize 实现数据驱动，每条异常数据独立成用例。

运行测试：`pytest test_disabletag.py -v
