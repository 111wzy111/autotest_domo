import requests
import json
import pytest
import api
#$env:REQUESTS_CA_BUNDLE = "E:\auto test\beisen\证书\证书.pem"
@pytest.fixture(scope="session")
def token():
    print("\n===== 正在获取 token =====")
    return api.get_token()
@pytest.fixture(scope="session")
def tag_id(token):
    return api.get_tag_id(token)

class TestTagDisable:
    # def setup_method(self):
    #     """每个测试方法前执行，获取一次 token"""
    #     self.token = get_token()


    def test_disable_existing_tag(self,token,tag_id):


        resp = api.disable_tag(token, tag_id)
        assert resp.status_code == 200
        json_data = resp.json()
        assert json_data.get("code") == "200"
        assert "操作成功" in json_data.get("message", "")
    #

    def test_enable_existing_tag(self,token,tag_id):

        resp=api.enable_tag(token,tag_id)
        assert resp.status_code==200

    @pytest.mark.parametrize("invalid_tag_id",[
        "existent_id_123",
        "existent123",
        "",
        " "
    ])
    def test_nonexistent_tag(self,token,invalid_tag_id):
        resp = api.disable_tag(token, invalid_tag_id)
        assert resp.status_code == 200   # 假设HTTP层面仍然成功
        json_data = resp.json()
        assert json_data.get("code") != "200"
        data_list=json_data.get("data")
        if not data_list or len(data_list)== 0:
            pytest.fail(f"响应中的 data 字段为空或不存在，无法获取错误信息。完整响应：{json_data}")
        else:
            fail_message = data_list[0].get("failMessage")
        if invalid_tag_id=='':
            assert "标签编码不能为空" ==fail_message
        else:
            assert "标签不存在" == fail_message


    def test_delete_userstag(self,token,tag_id):
        resp=api.delete_usertag(token,tag_id)
        assert resp.status_code== 200
        json_data=resp.json()
        assert json_data.get("message")=="执行成功"

    def test_add_userstag(self, token, tag_id):
        resp = api.add_usertag(token, tag_id)
        assert resp.status_code == 200
        json_data = resp.json()
        assert json_data.get("message") == "执行成功"



