import requests
import time
import json


# 打开setup_mode
def Setup_modeON(headers,server,Device_id):
    ads_url = "https://ads%s/apiv1/devices/%s/cmds/setup_mode.json?env=ssct&value=1" %(server,Device_id)
    data = json.dumps({"device_id":Device_id,"value":"1"})
    try:
        res_control = requests.put(url=ads_url, headers=headers, data=data).json()
    except Exception as e:
        # print('Setup_modeON请求超时')
        # time.sleep(1)
        # Setup_modeON()
        return 'Setup_modeON NO'
    return 'Setup_modeON OK'

# 关闭setup_mode
def Setup_modeOFF(headers,server,Device_id):
    ads_url = "https://ads%s/apiv1/devices/%s/cmds/fetch_setup_mode.json?env=ssct" %(server,Device_id)
    data = json.dumps({"device_id":Device_id})
    try:
        res_control = requests.put(url=ads_url, headers=headers, data=data).json()
    except Exception as e:
        # print('Setup_modeOFF请求超时')
        # time.sleep(1)
        # Setup_modeOFF()
        return 'Setup_modeOFF NO'
    return 'Setup_modeOFF OK'

# 获取当前setup_mode
def Setup_modeNOW(headers,server,Device_id):
    ads_url = "https://ads%s/apiv1/devices/%s/cmds/setup_mode.json?env=ssct" %(server,Device_id)
    data = json.dumps({"device_id":Device_id,"value":"1"})
    try:
        res_control = requests.put(url=ads_url, headers=headers, data=data).json()
    except Exception as e:
        # print('Setup_modeNOW请求超时')
        # time.sleep(1)
        # Setup_modeNOW()
        return 'Setup_modeNOW NO'
    return 'Setup_modeNOW OK'

# 设备软重启
def Reboot(headers,server,Device_id):
    ads_url = "https://ads%s/apiv1/devices/%s/cmds/reboot.json?env=ssct" %(server,Device_id)
    data = json.dumps({"device_id":Device_id,"value":"0"})
    try:
        res_control = requests.put(url=ads_url, headers=headers, data=data).json()
    except Exception as e:
        # print('Reboot请求超时')
        # time.sleep(1)
        # Reboot()
        return 'Reboot NO'
    return 'Reboot OK'


# 设备硬重启
def Reboot1(headers,server,Device_id):
    ads_url = "https://ads%s/apiv1/devices/%s/cmds/reboot.json?env=ssct" %(server,Device_id)
    data = json.dumps({"device_id":Device_id,"value":"1"})
    try:
        res_control = requests.put(url=ads_url, headers=headers, data=data).json()
    except Exception as e:
        # print('Reboot1请求超时')
        # time.sleep(1)
        # Reboot1()
        return 'Reboot1 NO'
    return 'Reboot1 OK'

# 恢复出厂
def Factory_reset(headers,server,Device_id):
    ads_url = "https://ads%s/apiv1/devices/%s/cmds/factory_reset.json?env=ssct" %(server,Device_id)
    data = json.dumps({"device_id":Device_id})
    try:
        res_control = requests.put(url=ads_url, headers=headers, data=data).json()
    except Exception as e:
        # print('Factory_reset请求超时')
        # time.sleep(1)
        # Factory_reset()
        return 'Factory_reset NO'
    return 'Factory_reset OK'


# 开启日志
def LogON(headers,server,Device_id):
    ads_url = "https://ads%s/apiv1/devices/%s/cmds/log.json?env=ssct" %(server,Device_id)
    data = json.dumps({"device_id":Device_id,"value":"1"})
    try:
        res_control = requests.put(url=ads_url, headers=headers, data=data).json()
    except Exception as e:
        # print('LogON请求超时')
        # time.sleep(1)
        # LogON()
        return 'LogON NO'
    return 'LogON OK'

# 关闭日志
def LogOFF(headers,server,Device_id):
    ads_url = "https://ads%s/apiv1/devices/%s/cmds/log.json?env=ssct" %(server,Device_id)
    data = json.dumps({"device_id":Device_id,"value":"0"})
    try:
        res_control = requests.put(url=ads_url, headers=headers, data=data).json()
    except Exception as e:
        # print('LogOFF请求超时')
        # time.sleep(1)
        # LogOFF()
        return 'LogOFF NO'
    return 'LogOFF OK'


# 开启LAN模式
def LanON(headers,server,Device_id):
    ads_url = "https://ads%s/apiv1/devices/%s/lan.json?env=ssct" %(server,Device_id)
    data = json.dumps({"lan_shared_secret":{"keep_alive":30,"lanip_key_lifetime":15552000,"auto_sync":"true"}})
    try:
        res_control = requests.post(url=ads_url, headers=headers, data=data).json()
    except Exception as e:
        # print('LanON请求超时')
        # time.sleep(1)
        # LanON()
        return 'LanON NO'
    return 'LanON OK'


# 关闭LAN模式
def LanOFF(headers,server,Device_id):
    ads_url = "https://ads%s/apiv1/devices/%s/lan.json?env=ssct" %(server,Device_id)
    # data = json.dumps({})
    try:
        res_control = requests.delete(url=ads_url, headers=headers).json()
    except Exception as e:
        # print('LanOFF请求超时')
        # time.sleep(1)
        # LanOFF()
        return 'LanOFF NO'
    return 'LanOFF OK'

# 设置时区
def TimeZone(headers,server,Device_id):
    ads_url = "https://ads%s/apiv1/devices/%s/time_zones.json?env=ssct&device_id=%s" %(server,Device_id,Device_id)
    data = json.dumps({"device_id":Device_id,"time_zone":{"dst":"false","dst_active":"false","dst_next_change_date":None,"dst_next_change_time":None,"tz_id":"Asia/Shanghai","utc_offset":"+08:00","key":"1571"}})
    try:
        res_control = requests.post(url=ads_url, headers=headers, data=data).json()
    except Exception as e:
        # print('LanON请求超时')
        # time.sleep(1)
        # LanON()
        return 'TimeZone NO'
    return 'TimeZone OK'


# 删除所有指令
def DeleteAllCommand(headers,server,Device_id):
    ads_url = "https://ads%s/apiv1/devices/%s/cmds.json?env=ssct" % (server, Device_id)
    # data = json.dumps({})
    try:
        res_control = requests.delete(url=ads_url, headers=headers).json()
    except Exception as e:
        # print('DeleteAllCommand请求超时')
        # time.sleep(1)
        # DeleteAllCommand()
        return 'DeleteAllCommand NO'
    return 'DeleteAllCommand OK'

