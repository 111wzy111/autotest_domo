# autotest_domo
基于Python+requests的接口自动化测试示例，包含token的获取，标签的获取，包含标签的停用、启用、异常场景等，以及给人打标签、给人移除标签的端到端场景
对于核心接口增加超时判断以及重试机制，并通过 Charles 模拟弱网验证
运行测试：pytest test_disabletag.py -v
