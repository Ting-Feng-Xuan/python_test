# -*- coding: utf-8 -*-
from xlutils.copy import copy
import xlrd
import requests
import time
import json

# 获取token
def login(username, password):
    url = "https://dashboard.sunseaiot.com/sessions"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    data = {"email": username, "password": password}
    try:
        res = requests.post(url=url, headers=headers, data=data, timeout=20, allow_redirects=False)
    except Exception as e:
        print('登录超时')
        time.sleep(1)
        login(username, password)
    print(res.text)
    print(res.headers["Location"])
    global USER_LOGIN_TOKEN
    USER_LOGIN_TOKEN = res.headers["Location"].split('/')[-1]
    print(USER_LOGIN_TOKEN)
    return USER_LOGIN_TOKEN

# 获取当前时间
def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    # data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_head = time.strftime("%H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    print(time_stamp)
    return time_stamp

# 通过DSN获取设备的ID
def GetDeviceID(headers,server,DSN):
    ads_url = "https://ads-field2.%s/apiv1/dsns/%s.json?env=ssct" % (server,DSN)
    try:
        res_info = requests.get(url=ads_url, headers=headers).json()
    except Exception as e:
        print('状态查询超时2')
        time.sleep(1)
        GetDeviceID()
    DeviceID = str(res_info['device']['id'])
    return DeviceID

# 设备硬重启
def Reboot1(headers,server,Device_id):
    ads_url = "https://ads-field2.%s/apiv1/devices/%s/cmds/reboot.json?env=ssct" %(server,Device_id)
    data = json.dumps({"device_id":Device_id,"value":"1"})
    try:
        res_control = requests.put(url=ads_url, headers=headers, data=data).json()
    except Exception as e:
        # print('Reboot1请求超时')
        # time.sleep(1)
        # Reboot1()
        return 'Reboot1 NO'
    return 'Reboot1 OK'


# 将数据写入excel文件,path:excel文件路径,row:行数,data:写入的数据
def write_excel(path,row,time,data,data1,time1):
    rb = xlrd.open_workbook(path)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    ws.write(row,1,data)
    ws.write(row,2,time)
    ws.write(row,3,data1)
    ws.write(row,4,time1)
    wb.save(path)


if __name__ == '__main__':

    server = 'ayla.com.cn'
    # 登陆
    username = input('Please input username = ')
    password = input('Please input password = ')
    DSN = input('Please input DSN = ') # 需要控制设备的DSN
    ct = time.time()
    access_token = login(username, password)
    headers = {'content-type': "application/json",
               'authorization': "auth_token" + " " + access_token,
               }
    Device_id = GetDeviceID(headers, server, DSN)

    # 输入执行次数
    count = int(input("How many times do you want to execute? Please input the number（1～999999999）=   "))
    if count not in range(1,1000000000) :
        exit('sorry,Invalid number!')

    # 输入执行间隔时间
    interval_time = int(input("Please input the interval time (5~20000) = "))
    if interval_time not in range(5,20001) :
        exit('sorry,Invalid number!')

    for i in range(count):
        i=i+1
        print('===== 第 %s 轮执行指令 =====' % i)
        NowTime = time.time()
        if NowTime - ct > 36000:
            ct = NowTime
            access_token = login(username, password)
            headers = {'content-type': "application/json",
                       'authorization': "auth_token" + " " + access_token,
                       }
        Resert = Reboot1(headers, server, Device_id)
        time.sleep(interval_time)


