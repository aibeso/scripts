#coding=utf-8
# 在这里输入青龙面板用户名密码，如果不填写，就自动从auth.json中读取
username = ""
password = ""

import random
import requests
import time
import json
import re
from urllib.parse import urlencode

requests.packages.urllib3.disable_warnings()

token = ""
if username == "" or password == "":
    f = open("/ql/config/auth.json") 
    auth = f.read()
    auth = json.loads(auth)
    username = auth["username"]
    password = auth["password"]
    token = auth["token"]
    f.close()

# 随机获取sign
def randomData():
    dataList = ['clientVersion=10.0.10&build=89313&client=android&d_brand=HUAWEI&d_model=&osVersion=10&screen=&partner=huawei&oaid=9dea5df4-ac2c-42c2-8e3d-3fd22701d28d&openudid=2dae0e93db0d6c76&eid=eidA0ae181230fs4CSxdiHhXRUW6VS8Agggh9AksXwK/bY1qxta7uHosJeEFD+HrgxWgzk4zJc2RUe96AutjvB58jpfBLHlUHQgoH/gZeaDvhWdJvm1K&sdkVersion=29&lang=zh_CN&uuid=2dae0e93db0d6c76&aid=2dae0e93db0d6c76&area=20_1715_43117_59197&networkType=wifi&wifiBssid=87755076efd23356df49215c25d4db18&uts=0f31TVRjBSsqndu4%2FjgUPz6uymy50MQJM8skMS8GqS7Mova%2FC0EcnIzmr6SIBLGZMdgshsZta%2FQHKflJ77HEktP7ju2dYO3drkizj2mW6dYxGFSlph6zf9ZG%2B%2FWyyIWhk8P5gpmbO7IAR3IUIBmfJL7AEN%2FXXDAlgVdfctYrQUvn4CFETnYB9qgLBnvuaz7%2F522dEZ26GmB5MTg3hp8Zyg%3D%3D&uemps=0-2&harmonyOs=1&st=1630550533108&sign=98d1f20b12b97e0781d224029c44528b&sv=102',
           'clientVersion=10.0.10&build=89313&client=android&d_brand=HUAWEI&d_model=&osVersion=10&screen=&partner=huawei&oaid=9dea5df4-ac2c-42c2-8e3d-3fd22701d28d&openudid=2dae0e93db0d6c76&eid=eidA0ae181230fs4CSxdiHhXRUW6VS8Agggh9AksXwK/bY1qxta7uHosJeEFD+HrgxWgzk4zJc2RUe96AutjvB58jpfBLHlUHQgoH/gZeaDvhWdJvm1K&sdkVersion=29&lang=zh_CN&uuid=2dae0e93db0d6c76&aid=2dae0e93db0d6c76&area=20_1715_43117_59197&networkType=wifi&wifiBssid=unknown&uts=0f31TVRjBSsqndu4%2FjgUPz6uymy50MQJusRA8XoJqZz7kwDvTQ%2BCB8ji1htLgWHegbSeVZFqTqUBYx1lpxnlJCOjZ%2Bnc%2FHdWSHDbndHpF7pchMKcm4Pi6vYKrZ7v8%2B81wql6iJvH5iJWsekzW2fWjAb6W0cRsMBRdJPpJVTciUk4sExwmtpjSicTRBSIj%2BVGMzd7tG1FE1iSJtYGWbEd4A%3D%3D&uemps=0-2&harmonyOs=1&st=1630552132013&sign=f035279d30887e587c7ba14e5ac58463&sv=122', 
            ] #  data1 就是从genToken里获取到的参数 自己填写下吧
    index = random.randint(0, len(dataList)-1)
    return dataList[index]
    print('使用的是第'+ str(index) + '随机sign')
    return dataList[index]

def gettimestamp():
    return str(int(time.time() * 1000))


def login(username, password):
    url = "http://127.0.0.1:5700/api/login?t=%s" % gettimestamp()
    data = {"username": username, "password": password}
    r = s.post(url, data)
    s.headers.update({"authorization": "Bearer " + json.loads(r.text)["data"]["token"]})


def getitem(key):
    url = "http://127.0.0.1:5700/api/envs?searchValue=%s&t=%s" % (key, gettimestamp())
    r = s.get(url)
    item = json.loads(r.text)["data"]
    return item


def getckitem(key):
    url = "http://127.0.0.1:5700/api/envs?searchValue=JD_COOKIE&t=%s" % gettimestamp()
    r = s.get(url)
    for i in json.loads(r.text)["data"]:
        if key in i["value"]:
            return i
    return []


def wstopt(cookies):
    headers = {
        'user-agent': 'okhttp/3.12.1;jdmall;android;version/10.0.10;build/89313;screen/1080x2259;os/10;network/wifi;',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookies,
    }
    url = 'https://api.m.jd.com/client.action?functionId=genToken&' + randomData()
    body = 'body=%7B%22to%22%3A%22https%253a%252f%252fplogin.m.jd.com%252fjd-mlogin%252fstatic%252fhtml' \
           '%252fappjmp_blank.html%22%7D&'
    response = requests.post(url, data=body, headers=headers, verify=False)
    data = json.loads(response.text)
    if data.get('code') != '0':
        return None
    tokenKey = data.get('tokenKey')
    url = data.get('url')
    session = requests.session()
    params = {
        'tokenKey': tokenKey,
        'to': 'https://plogin.m.jd.com/jd-mlogin/static/html/appjmp_blank.html'
    }
    url += '?' + urlencode(params)
    session.get(url, allow_redirects=True)
    result = ""
    for k, v in session.cookies.items():
        if k == 'pt_key' or k == 'pt_pin':
            result += k + "=" + v + "; "
    return result


def update(text, qlid):
    url = "http://127.0.0.1:5700/api/envs?t=%s" % gettimestamp()
    s.headers.update({"Content-Type": "application/json;charset=UTF-8"})
    data = {
        "name": "JD_COOKIE",
        "value": text,
        "_id": qlid
    }
    r = s.put(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return False


def insert(text):
    url = "http://127.0.0.1:5700/api/envs?t=%s" % gettimestamp()
    s.headers.update({"Content-Type": "application/json;charset=UTF-8"})
    data = []
    data_json = {
        "value": text,
        "name": "JD_COOKIE"
    }
    data.append(data_json)
    r = s.post(url, json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    s = requests.session()
    if token == "":
        login(username, password)
    else:
        s.headers.update({"authorization": "Bearer " + token})
    wskeys = getitem("JD_WS_CK")
    count = 1
    for i in wskeys:
        if i["status"]==0:
            ptck = wstopt(i["value"])
            wspin = re.findall(r"pin=(.*?);", i["value"])[0]
            item = getckitem("pt_pin=" + wspin)
            if item != []:
                qlid = item["_id"]
                if update(ptck, qlid):
                    print("第%s个wskey更新成功, pin:%s" % (count, wspin))
                else:
                    print("第%s个wskey更新失败, pin:%s" % (count, wspin))
            else:
                if insert(ptck):
                    print("第%s个wskey添加成功" % count)
                else:
                    print("第%s个wskey添加失败" % count)
            count += 1
        else:
            print("有一个wskey被禁用了")
