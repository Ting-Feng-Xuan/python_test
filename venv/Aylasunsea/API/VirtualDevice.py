import requests
import time
import json
from datetime import datetime
from Aylasunsea.API.login import login



# 创建虚拟设备
def CreateVirtualDevices(headers,path,uuid):
    t = str(datetime.utcnow())
    f = open(path, 'a')
    ads_url = "https://ads-dev.sunseaiot.com/deviceservice/v1/virtual_devices.json?env=ssct"
    for i in range(21,23):
        data = json.dumps({"oem_model": "rtk-ledevb","product_name":"gu%s" %i})
        try:
          res_control = requests.post(url=ads_url, headers=headers, data=data).json()
        except Exception as e:
            print('控制请求超时1')
            time.sleep(1)
            CreateVirtualDevices()
        DSN = res_control["device"]["dsn"]

        Register = VirtualDevicesRegister(headers,DSN,uuid)
        DeviceID = GetDeviceID(headers,DSN)
        Template = VirtualDevicesTemplate(headers, DeviceID)
        Online = VirtualDevicesOnline(headers,DeviceID)
        print(DSN)
        # f.write(DSN)
        f.writelines([DSN, ',', DeviceID])
        f.write('\n')
    f.close()
    return t


# 通过DSN获取设备的ID
def GetDeviceID(headers,DSN):
    ads_url = "https://ads-dev.sunseaiot.com/apiv1/dsns/%s.json?env=ssct" % DSN
    try:
        res_info = requests.get(url=ads_url, headers=headers).json()
    except Exception as e:
        print('状态查询超时2')
        time.sleep(1)
        GetDeviceID()
    DeviceID = str(res_info['device']['id'])
    return DeviceID


# 把设备绑定给指定的用户
def VirtualDevicesRegister(headers,dsn,uuid):
    t = str(datetime.utcnow())
    ads_url = "https://ads-dev.sunseaiot.com/apiv1/devices/%s/register.json?env=ssct" % dsn
    data = json.dumps({"user_uuid":uuid})
    try:
        res_control = requests.put(url=ads_url, headers=headers, data=data).json()
    except Exception as e:
        # print('控制请求超时3')
        time.sleep(1)
        # VirtualDevicesRegister()
    return t


# 为设备设定特定的模版
def VirtualDevicesTemplate(headers,Device_id):
    t = str(datetime.utcnow())
    Template_id = str(2479)
    ads_url = "https://ads-dev.sunseaiot.com/apiv1/devices/%s/template/%s.json?env=ssct" % (Device_id,Template_id)
    data = json.dumps({"device_id":Device_id,"template_id":Template_id})
    try:
        res_control = requests.put(url=ads_url, headers=headers, data=data).json()
    except Exception as e:
        # print('控制请求超时3')
        time.sleep(1)
        # VirtualDevicesTemplate()
    return t


# 创建设备的连接记录为Online,使设备上线
def VirtualDevicesOnline(headers,Device_id):
    t = str(datetime.utcnow())
    ads_url = "https://ads-dev.sunseaiot.com/apiv1/devices/%s/connection_history.json" % Device_id
    data = json.dumps({"connection": {"event_time":t,"status":"Online"}})
    try:
        res_control = requests.post(url=ads_url, headers=headers, data=data).json()
    except Exception as e:
        print('控制请求超时4')
        time.sleep(1)
        VirtualDevicesOnline()

    Event_time = res_control["connection_history"]["event_time"]
    Status = res_control["connection_history"]["status"]
    return Event_time,Status

# 创建设备的连接记录为Offline,使设备上线
def VirtualDevicesOffline(headers,Device_id):
    t = str(datetime.utcnow())
    ads_url = "https://ads-dev.sunseaiot.com/apiv1/devices/%s/connection_history.json" % Device_id
    data = json.dumps({"connection": {"event_time":t,"status":"Offline"}})
    try:
        res_control = requests.post(url=ads_url, headers=headers, data=data).json()
    except Exception as e:
        print('控制请求超时')
        time.sleep(1)
        VirtualDevicesOffline()

    Event_time = res_control["connection_history"]["event_time"]
    Status = res_control["connection_history"]["status"]
    return Event_time,Status


if __name__ == '__main__':
    url = "https://dashboard-dev.sunseaiot.com/sessions/create"
    path = "/Users/doctorgu/Desktop/auto_test/Aylasunsea/txt/DeviceList.txt"
    username = "guyisheng@sunseaaiot.com"
    password = "Hsxy1008"
    user_uuid = "38600fec-ed52-11e8-a347-0a580ae94ea6"
    headers = login(url, username, password)

    # 创建虚拟设备并把DSN保存到txt文件中
    CreateVirtualDevices = CreateVirtualDevices(headers,path,user_uuid)

    # 读取txt文件中到DSN，并绑定用户
    # VirtualDevicesRegister = VirtualDevicesRegister(headers, 'VD7734c0fa0000617', user_uuid)
    # f = open(path,'r')
    # readline = f.readlines()
    # for i in readline:
    #     DSN = i.strip()
    #     print(DSN)
    #     VirtualDevicesRegister = VirtualDevicesRegister(headers,DSN,user_uuid)
    #     time.sleep(3)

    # 创建设备的连接记录为Online,使设备上线
