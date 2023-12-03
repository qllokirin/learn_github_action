import requests
from datetime import datetime   
token="f423ff08b81a499ba66f6f5f2b488ff5"

def plus_plus():
    global token
    response = requests.post(
        url="https://www.pushplus.plus/send/",
        json={"token": token,
        "title":"测试github action~",
        "content": "当前时间：{}".format(datetime.now())
        }
    )
    if response.status_code == 200:
        print("成功发送(或许)")
        print("消息流水号:",response.json()["data"])
print(datetime.now())
plus_plus()