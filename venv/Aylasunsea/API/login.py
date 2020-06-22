import requests
import time


# 通过username、password返回hesders
def login(url, username, password):

    header = {"content-type": "application/x-www-form-urlencoded"}
    data = {"email": username, "password": password}
    for i in range(3):
        try:
            res = requests.post(url=url, headers=header, data=data, timeout=20, allow_redirects=False)
            break
        except Exception as e:
            print('登录超时')
            time.sleep(1)
            #login(url,username, password)
            continue
        # print(res.text)
        # print(res.headers["Location"])
    global USER_LOGIN_TOKEN
    USER_LOGIN_TOKEN = res.headers["location"].split('/')[-1]
    print(USER_LOGIN_TOKEN)
    headers = {'content-type': "application/json",'authorization': "auth_token" + " " + USER_LOGIN_TOKEN,}
    return headers

def login_rout(url,password):
    header = {"content-type": "application/x-www-form-urlencoded"}
    data = {}