import requests
import time
import json
from Aylasunsea.Public_Module.Time_Now import Time_timezone
import datetime


# 获取所有属性的详细信息
def GetGropertieList(headers,server,Device_ID):
    ads_url = "https://ads%s/apiv1/devices/%s/properties.json?env=ssct"%(server,Device_ID)
    print(ads_url)
    res_list = []
    req_count = 0
    print("loading",end="")
    for i in range(6):
        try:
            res_list = requests.get(url=ads_url, headers=headers).json()
            break
        except Exception as e:
            print('.',end="")
            print("erroe:", e.msg)
            time.sleep(1)
            #GetGropertieList(headers,server,Property_num)
            req_count += 1
            continue
    print("")
    if req_count == 6:
        print("状态查询超时")
    print(res_list)
    return res_list
    # try:
    #     # name = res_status['property']['name']
    #     value = res_list['property']['value']
    #     time_up = res_list['property']['data_updated_at']
    #     Time_up = time_up[11:19]
    # except Exception as e:
    #     time.sleep(1)
    #     GetGropertieList()
    # return value,Time_up



# 创建数据点,Property_num对应属性的ID,datapoint数据点的值
def PostPropertieDatapoint(headers,server,TimeZone,Property_num,datapoint):
    # 设备控制api
    # ads_url = "https://ads-%s/apiv1/properties/%s/datapoints.json?env=ssct" % (server,Property_num)
    ads_url = "https://ads%s/apiv1/properties/%s/datapoints.json?env=ssct" % (server,Property_num)
    # headers = get_token()
    data = json.dumps({"id": Property_num, "datapoint": {"value": datapoint}})
    try:
        res_control = requests.post(url=ads_url, headers=headers, data=data).json()
    except Exception as e:
        print('控制请求超时')
        time.sleep(1)
        PostPropertieDatapoint()
    # print(res_control)
    time_up = res_control["datapoint"]["updated_at"]
    # update_time = Update_time[11:19]
    data = res_control["datapoint"]["value"]

    update_time = Time_timezone(TimeZone, time_up)
    Update_time = update_time[0]
    Update_utc = update_time[1]

    print("%s = %s" %(Property_num,datapoint))



    return data,Update_time,Update_utc
    # time.sleep(3)

def GetTimeZoneInfo(headers,server,ddevice_id):
    ads_url = "https://ads%s/apiv1/devices/%s/time_zones?env=ssct"%(server,device_id)
    try:
        res_result = requests.get(url=ads_url, headers=headers).json()
    except Exception as e:
        print(e.msg)
    return res_result
# 获取该属性的详细信息，包括name、value、data_updated_at
def GetPropertieInfo(headers,server,TimeZone,Property_num):
    # ads_url2 = "https://ads-dev.sunseaiot.com/apiv1/properties/%s"%num + ".json?env=ssct"
    ads_url = "https://ads%s/apiv1/properties/%s.json?env=ssct" % (server,Property_num)
    # headers = get_token()
    try:
        res_info = requests.get(url=ads_url, headers=headers).json()
    except Exception as e:
        print('状态查询超时')
        time.sleep(1)
        GetPropertieInfo()
    try:
        # name = res_status['property']['name']
        value = res_info['property']['value']
        time_up = res_info['property']['data_updated_at']
        # print(time_up)
        # Time_up = time_up[11:19]

        update_time = Time_timezone(TimeZone, time_up)
        Update_time = update_time[0]
        Update_utc = update_time[1]

    except Exception as e:
        time.sleep(1)
        GetPropertieInfo()

    return value,Update_time,Update_utc
    # print(res_status['property']['name'], res_status['property']['value'])
    # return (name, value)