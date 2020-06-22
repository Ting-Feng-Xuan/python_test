import requests
import time
import json
import random
from Aylasunsea.API.login import login
from Aylasunsea.API.DeviceControl import Setup_modeNOW
from Aylasunsea.API.DeviceControl import Setup_modeON
from Aylasunsea.API.DeviceControl import Setup_modeOFF
from Aylasunsea.API.DeviceControl import Factory_reset
from Aylasunsea.API.DeviceControl import Reboot
from Aylasunsea.API.DeviceControl import Reboot1
from Aylasunsea.API.DeviceControl import LanON
from Aylasunsea.API.DeviceControl import LanOFF
from Aylasunsea.API.DeviceControl import LogON
from Aylasunsea.API.DeviceControl import LogOFF
from Aylasunsea.API.DeviceControl import TimeZone
from Aylasunsea.API.schedule import Schedule
from Aylasunsea.API.DeviceControl import DeleteAllCommand
from Aylasunsea.API.OTA import CreatOTAjob
from Aylasunsea.API.OTA import StartOTAjob
from Aylasunsea.API.OTA import GetOTAstatus
from Aylasunsea.API.Properties import PostPropertieDatapoint


if __name__ == '__main__':

    # 输入设备所在的域的oem_id
    oem_id = '3c75973b'
    if oem_id == '495c64f1' :   #量产域
        url = 'https://dashboard.sunseaiot.com/sessions'
        server = '-field2.ayla.com.cn'
    elif oem_id == '7734c0fa' :    #旧开发域，所有服务和量产域一样
        url = 'https://dashboard.sunseaiot.com/sessions'
        server = '-field2.ayla.com.cn'
    else:
        oem_id = '3c75973b'    #开发域
        url = 'https://dashboard-as-dev.sunseaiot.com/sessions'
        server = '-dev.ayla.com.cn'
    # 登陆账号
    username = "guyisheng@sunseaaiot.com"
    password = "Hsxy1008"
    # 设备信息
    DSN = 'AC000W009232209'
    Device_id = '15692467'
    # sch_id = 1092844
    # Property = 576571
    # Property_model =  576573
    Property = [580293,580294,580299]    #多个属性同时测试
    value = [1,0]
    # jv_ctrl属性的值
    # ct = time.time()
    # value = '{"cmd":1,"utc":%s}'%ct
    # 登陆
    headers = login(url, username, password)
    # 执行的次数
    for k in range(99999):
        k = k+1
        print('第 %s 次OTA' % k)
        if k%2 ==0:

            OTAData = {"group_id":"679","image_id":1815,"ignore_invalid":'true',"name":"bk-1.0.2","sw_version":"1.0.2"}

        else:

            OTAData = {"group_id":"679","image_id":1813,"ignore_invalid":'true',"name":"bk-1.0.1","sw_version":"1.0.1-2"}

        jobID = CreatOTAjob(headers, server,OTAData)      #创建OTA任务
        print(jobID)
        Starjob = StartOTAjob(headers, server,jobID)     #执行OTA任务

        time.sleep(10)
        i = 0
        Getstatus = GetOTAstatus(headers,server,jobID)     #获取OTA任务的状态
        while Getstatus != 1:        # 1代表OTA成功
            i += 1
            print('第 %s 次OTA,第 %s 轮指令' % (k, i))
            # print('第 %s 轮,设备 %s 执行指令' % (k, Device_id))
            setup_modeON = Setup_modeON(headers,server,Device_id)    #打开setup_mode
            print(setup_modeON)
            time.sleep(1)
            setup_modeOFF = Setup_modeOFF(headers, server, Device_id)    #关闭setup_mode
            print(setup_modeOFF)
            time.sleep(1)
            setup_modeNOW = Setup_modeNOW(headers, server, Device_id)    #读取当前setup_mode
            print(setup_modeNOW)
            time.sleep(1)
            # root = Reboot(headers, server, Device_id)    #设备软重启
            # print(root)
            # time.sleep(1)
            # root1 = Reboot1(headers,server,Device_id)    #设备硬重启
            # print(root1)
            # time.sleep(1)
            # factory_reset = Factory_reset(headers, server, Device_id)    #设备恢复出厂设置
            # print(factory_reset)

            logON = LogON(headers, server, Device_id)    #打开日志服务
            print(logON)
            time.sleep(1)
            logOFF = LogOFF(headers, server, Device_id)    #关闭日志服务
            print(logOFF)
            time.sleep(1)
            # lanON = LanON(headers, server, Device_id)    #打开LAN模式
            # print(lanON)
            # time.sleep(1)
            # lanOFF = LanOFF(headers, server, Device_id)    #关闭LAN模式
            # print(lanOFF)
            # time.sleep(1)
            timezone = TimeZone(headers, server, Device_id)    #设置时区
            print(timezone)
            time.sleep(1)
            # T = 10
            # sch = Schedule(headers, server, Device_id,sch_id,T)    #设置定时任务在T秒后执行
            # time.sleep(1)
            # PostPropertieDatapoint(headers, server, Property, 1)   #设置属性的值为1
            # time.sleep(1)
            # PostPropertieDatapoint(headers, server, Property, 0)   #设置属性的值为0
            for j in range(10):

                PostPropertieDatapoint(headers, server, random.choice(Property), random.choice(value))   #随机选择属性，随机匹配值
            # PostPropertieDatapoint(headers, server, random.choice(Property_model), random.randint(1,11))  #随机选择属性，随机匹配值
                time.sleep(random.randint(1,5))       #设置随机等待时间
            # 获取当前utc时间
            # ct = time.time()
            # value = '{"cmd":1,"utc":%s}' % ct
            # PostPropertieDatapoint(headers, server, Property_num2,value )   #设置jv_ctrl属性的值

            Getstatus = GetOTAstatus(headers,server,jobID)     #获取OTA任务的状态

        if k % 10 == 0:     #每N轮循环清除一次堆积的指令
            time.sleep(60)
            for i in range(5):    #清除指令的循环执行N遍
                deleteAll = DeleteAllCommand(headers,server,Device_id)
                print(deleteAll)