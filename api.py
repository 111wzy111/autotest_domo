import requests
import json
import time

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

def get_tag_id(token):
    tag_id = None
    tag_name = "auto_addtag"
    all_tag = get_tag(token)
    tag_list = all_tag.get("data")
    for tag in tag_list:
        if tag["name"] == f"{tag_name}":
            tag_id = tag["code"]
            break
    return tag_id
def disable_tag(token,tag_id):
    for i in range(3):
        try:
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
            response = requests.request("post", url, headers=header, data=body,timeout=3)
            if response.status_code == 200:
                return response
        except requests.exceptions.Timeout:
            if i ==2:
                raise
            time.sleep(2)

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

def add_usertag(token,tag_id):
    url='https://openapi.italent.link/DataCenterApi/api/v1/EmployeeTag/AddUsersEmployeeTags'
    header={
        "Authorization":f"Bearer {token}"
    }
    body={
        "employeeTags":
            [
                {
                    "userID": "662519962",
                    "tagCode": f"{tag_id}"
                }
            ]
    }
    response=requests.request("post",headers=header,url=url,json=body)

    return response

def delete_usertag(token,tag_id):
    url='https://openapi.italent.link/DataCenterApi/api/v1/EmployeeTag/DeleteUsersEmployeeTags'
    header={
        "Authorization":f"Bearer {token}"
    }
    body={
        "employeeTags":
            [
                {
                    "userID": "662519962",
                    "tagCode": f"{tag_id}"
                }
            ]
    }
    response=requests.request("post",headers=header,url=url,json=body)
    return response
