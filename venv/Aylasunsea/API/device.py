import requests
import time
import json


# 获取用户所有设备ID、DSN
def GetUserDevice(headers,username):
    ads_url = "https://ads-dev.sunseaiot.com/apiv1/devices/find_by_user_email.json?env=ssct&email=%s" % username
    res_list = []
    try:
        res_list = requests.get(url=ads_url, headers=headers).json()
    except Exception as e:
        print('状态查询超时')
        time.sleep(1)
        GetUserDevice()
    # print(res_list)
    return res_list