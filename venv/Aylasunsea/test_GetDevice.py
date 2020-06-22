import time
from Aylasunsea.API.Properties import GetGropertieInfo
from Aylasunsea.API.Properties import PostPropertieDatapoint
from Aylasunsea.API.login import login
from Aylasunsea.Public_Module.Time_Now import get_time_stamp
from Aylasunsea.Public_Module.write_excel import write_excel
from Aylasunsea.API.Properties import GetGropertieList
from Aylasunsea.API.device import GetUserDevice
import requests

if __name__ == '__main__':
    url = "https://dashboard-dev.sunseaiot.com/sessions/create"
    path = "/Users/doctorgu/Desktop/auto_test/Aylasunsea/txt/DeviceList.txt"
    # print('1、以当前时间为属性A的值')
    # print('2、以一定时间间隔发送属性A的值')
    # print('3、获取属性A在云端更新的时间')
    # print('4、设备端设置属性A的值变化时通过属性B上报相同的值')
    # print('5、获取属性B在云端更新的时间')
    # print('6、把获取到的所有数据保存在')
    username = "guyisheng@sunseaaiot.com"
    password = "Hsxy1008"
    # DSN = 'SC000W000122378'  # 需要控制设备的DSN
    Property_name = 'cmd'
    Property_name2 = 'log'
    headers = login(url, username, password)
    f = open(path, 'w')
    DeviceList = GetUserDevice(headers,username)
    for i in DeviceList:
        DSN = i['device']['dsn']
        ID = str(i['device']['id'])
        # print(DSN)
        # print(ID)
        # f.writelines([DSN,',',ID])
        if DSN[0] == 'V':
            # f.write(DSN,",",ID)
            f.writelines([DSN, ',', ID])
            f.write('\n')
    f.close()