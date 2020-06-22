import requests
import time

# 通过username、password返回access_token
def login(url, path,username, password):
    f = open(path, 'w')
    header = {"content-type": "application/x-www-form-urlencoded"}
    data = {"email": username, "password": password}
    try:
        res = requests.post(url=url, headers=header, data=data, timeout=20, allow_redirects=False)
    except Exception as e:
        print('登录超时')
        time.sleep(1)
        login(username, password)

    global USER_LOGIN_TOKEN
    USER_LOGIN_TOKEN = res.headers["Location"].split('/')[-1]
    print(USER_LOGIN_TOKEN)
    f.writelines(USER_LOGIN_TOKEN)

    return USER_LOGIN_TOKEN


if __name__ == '__main__':
    server = ['sunseaiot.com','ayla.com.cn','aylanetworks.com','aylanetworks.com','10646.cn']
    print("1.SA")
    print("2.CN")
    print("3.US")
    print("4.EU")
    print("5.CU")
    ServerInput = int(input("Please input the number = "))
    if ServerInput == 1:
        server = server[0]
    elif ServerInput == 2:
        server = server[1]
    elif ServerInput == 3:
        server = server[2]
    elif ServerInput == 4:
        server = server[3]
    elif ServerInput == 5:
        server = server[4]
    else:
        exit('sorry,Invalid number!')
    url = "https://dashboard-dev.%s/sessions/create" %server
    path = "auth_token.txt"
    # 登陆
    username = input('Please input username = ')
    password = input('Please input password = ')
    access_token = login(url,path, username, password)