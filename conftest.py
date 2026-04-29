import json

import pytest
import api
import os
def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: 冒烟测试用例")

@pytest.fixture(scope="session")
def token():
    print("\n===== 正在获取 token =====")
    return api.get_token()
@pytest.fixture(scope="session")
def tag_id(token):
    return api.get_tag_id(token)
@pytest.fixture(scope="session", autouse=True)
def global_setup():
    print("\n🏁 [Session] 整个测试会话开始前，执行一次全局初始化...")
    yield
    print("\n🏁 [Session] 整个测试会话结束后，执行一次全局清理...")

@pytest.fixture(scope="function")
def test_data(invalid_tag_id):
    data=f"测试数据{invalid_tag_id}"
    print(data)
    yield data
    print("清理数据")