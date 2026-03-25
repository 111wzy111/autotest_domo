import requests
import json
import pytest

def get_token():
  url = "https://openapi.italent.link/token"
  payload = json.dumps({
    "grant_type": "client_credentials",
    "app_key": "E10EB8CE21174248848E39E3BB07D72D",
    "app_secret": "EA6C65AC0EA5492E8467E5101B53974DD939A3D202604955B5C6CD8B39CB9007"
  })
  headers = {
    'Content-Type': 'application/json'
  }
  response = requests.request("POST", url, headers=headers, data=payload)
  if response.status_code == 200:
    result=response.json()
    token=result.get('access_token')
    return token
  else:
    print('获取Token失败，响应码：',response.status_code)
    print("响应内容：", response.text)
    return None

def get_tag(token):
    url="https://openapi.italent.link/DataCenterApi/api/v1/TalentTag/GetTags"
    headers={
        "Content-Type":"application/json",
        "Authorization":f"Bearer {token}"
    }
    payload={}
    response=requests.request("post",url,headers=headers,json=payload)
    return response.json()
def disable_tag(token,tag_id):
    url= "https://openapi.italent.link/DataCenterApi/api/v1/TalentTag/DisableTags"
    header={
        f"Authorization":f"Bearer {token}"
    }
    body=json.dumps({
        "tagCodes":
            [
                f"{tag_id}"
            ]
    })
    response = requests.request("post", url, headers=header, data=body)
    return response
def enable_tag(token,tag_id):
    url='https://openapi.italent.link/DataCenterApi/api/v1/TalentTag/EnableTags'
    header={
        "Authorization":f"Bearer {token}"
    }
    body={
        "tagCodes":
            [
                f"{tag_id}"
            ]
    }
    response=requests.request("post", url,headers=header,json=body)
    return response
@pytest.fixture(scope="session")
def token():
    print("\n===== 正在获取 token =====")
    return get_token()

class TestTagDisable:
    # def setup_method(self):
    #     """每个测试方法前执行，获取一次 token"""
    #     self.token = get_token()


    def test_disable_existing_tag(self,token):
        tag_id = None   # 替换成一个真实存在的标签ID
        tag_name = "auto_addtag"
        all_tag = get_tag(token)
        tag_list = all_tag.get("data")
        for tag in tag_list:
            if tag["name"] == f"{tag_name}":
                tag_id = tag["code"]
                break

        resp = disable_tag(token, tag_id)
        assert resp.status_code == 200
        json_data = resp.json()
        assert json_data.get("code") == "200"
        assert "操作成功" in json_data.get("message", "")
    #

    def test_enable_existing_tag(self,token):
        tag_id=None
        all_tag=get_tag(token)
        tag_list=all_tag.get("data")
        for tag in tag_list:
            if tag.get("name")=="auto_addtag":
                tag_id=tag.get("code")
                print(tag_id)
                break
        resp=enable_tag(token,tag_id)
        assert resp.status_code==200

    @pytest.mark.parametrize("invalid_tag_id",[
        "existent_id_123",
        "existent123",
        "",
        " "
    ])
    def test_nonexistent_tag(self,token,invalid_tag_id):
        resp = disable_tag(token, invalid_tag_id)
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



