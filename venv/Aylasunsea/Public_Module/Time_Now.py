import time
from datetime import datetime
import requests


# 时间戳转字符串
def get_time_stamp():
    ct = time.time()
    # print(ct)
    local_time = time.localtime(ct)
    # print(local_time)
    # data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_head = time.strftime("%H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    # print(time_stamp)
    # stamp = ("".join(time_stamp.split()[0].split("-")) + "".join(time_stamp.split()[1].split(":"))).replace('.', '')
    # print(stamp)
    # t = datetime.utcnow()
    # print(t)
    return time_stamp

# 时区的时间转换
def Time_timezone(TimeZone,time_up):
    time2 = time.strptime(time_up,"%Y-%m-%dT%H:%M:%SZ")
    ct = time.mktime(time2)
    utc = ct + TimeZone * 3600
    time3 = time.localtime(utc)
    Time = time.strftime("%H:%M:%S", time3)
    return Time,utc

# 获取时区
def get_TimeZone(headers,server,dsn):
    ads_url2 = "https://ads%s/apiv1/dsns/%s/time_zones.json?env=ssct" %(server,dsn)
    try:
        res_timezone = requests.get(url=ads_url2, headers=headers).json()
    except Exception as e:
        print('状态查询超时')
        time.sleep(1)
        get_TimeZone()
    TimeZone = res_timezone['time_zone']['utc_offset']
    return TimeZone