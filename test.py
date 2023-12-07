import requests
import os
import hashlib
import requests
TOKEN = os.environ["TOKEN"]
def plus_plus(content):
    requests.post(
        url="https://www.pushplus.plus/send/",
        json={"token": TOKEN,
        "title":"新的排考已经出现~",
        "content": content
        }
    )
def calculate_sha256(input_string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    return sha256_hash.hexdigest()

AUTH = os.environ["AUTH"]
response = requests.get(
    url="https://jwxt.nwpu.edu.cn/eams-micro-server/api/v1/exam/student/exam",
    headers={
        "Authorization": AUTH
    }
)
if response.status_code == 200:
    courses_data = response.json()["data"]
    if not courses_data:
        latest_course_sha256 = '0'
        print("暂未有排考")
    else:
        latest_course = courses_data[-1]['courseNameZh']+','+courses_data[-1]['examDate']+','+courses_data[-1]['place']
        latest_course_sha256 = calculate_sha256(latest_course)
        print("最新一门考试的哈希值：",latest_course_sha256)
    
    if os.path.isfile('courese'):
        with open('courese','r+') as f:
            if latest_course_sha256 == '0':
                print("暂未有排考")
                f.seek(0)
                f.truncate()
                f.write(latest_course_sha256)
            elif latest_course_sha256 == f.read():
                print("哈希值相等，未出现新的排考~")
            else:
                print("哈希值不等，新的排考已经出现!!")
                plus_plus(latest_course)
                f.seek(0)
                f.truncate()
                f.write(latest_course_sha256)
    else:
        with open('courese','w') as f:
            f.write(latest_course_sha256)
else:
    print('请求失败，状态码:', response.status_code)
    plus_plus("令牌过期了")