import time
import random
from Aylasunsea.API.Properties import GetGropertieList
from Aylasunsea.API.Properties import PostPropertieDatapoint
from Aylasunsea.API.login import login
from Aylasunsea.Public_Module.Time_Now import get_time_stamp
from Aylasunsea.Public_Module.write_excel import write_excel
from Aylasunsea.API.Properties import GetGropertieList

import Aylasunsea.URL.UrlLib

# 以当前时间为属性A的值
# 以一定时间间隔发送属性A的值
# 获取属性A在云端更新的时间
# 设备端设置属性A的值变化时通过属性B上报相同的值
# 获取属性B在云端更新的时间
# 把获取到的所有数据保存在
if __name__ == '__main__':
    sa_dev_url = "https://dashboard-as-dev.sunseaiot.com/sessions"
    path = "/Users/Sakura/Desktop/Python_test/date.csv"
    print('1、以当前时间为属性A的值')
    print('2、以一定时间间隔发送属性A的值')
    print('3、获取属性A在云端更新的时间')
    print('4、设备端设置属性A的值变化时通过属性B上报相同的值')
    print('5、获取属性B在云端更新的时间')
    print('6、把获取到的所有数据保存在:%s'%(path))
    username = "tangjun+cndevadmin@sunseaaiot.com"
    password = "465085410Tj"
    DSN = 'AC000W009647611'  # 需要控制设备的DSN
    Property_name = 'cmd'
    Property_name2 = 'log'
    headers = login(sa_dev_url, username, password)

    # for i in range(3):
    #     i=i+1
    #
    #     now_time = get_time_stamp()
    #     result = PostPropertieDatapoint(headers,"75319",now_time)
    #     time.sleep(2)
    #     result1 = GetGropertieInfo(headers,"75324")
    #     write_excel(path,i,result[0],result[1],result1[0],result1[1])
    #     time.sleep(2)
    #
    # result = []

    server = '-dev.ayla.com.cn'
    device_id="15693298"
    GropertieList = GetGropertieList(headers,server,"15693298")
    TimeZone = requests.get(TimeZoneUrl%(server,device_id))
    for i in GropertieList:
        name = i['property']['name']
        base_type = i['property']['base_type']
        direction = i['property']['direction']
        data_updated_at = i['property']['data_updated_at']
        key = i['property']['key']
        value = i['property']['value']

        if base_type == 'boolean' or base_type == ' integer' or base_type == 'decimal':
            time.sleep(2)
            Datapoint = PostPropertieDatapoint(headers,server,key,0)
            time.sleep(2)
            GropertieInfo = GetGropertieInfo(headers,key)
            if GropertieInfo[0] == 0 and Datapoint[1] == 0:
                print('%s=0 is ok'%name)
            else:
                print('%s=0 is Err' % name)
            time.sleep(2)
            Datapoint = PostPropertieDatapoint(headers,key,1)
            time.sleep(2)
            GropertieInfo = GetGropertieInfo(headers,key)
            if GropertieInfo[0] == 1 and Datapoint[1] == 1:
                print('%s=1 is ok'%name)
            else:
                print('%s=1 is Err' % name)
        else:
            time.sleep(2)
            Datapoint = PostPropertieDatapoint(headers,server,key,'0')
            time.sleep(2)
            GropertieInfo = GetGropertieInfo(headers,key)
            if GropertieInfo[0] == '0' and Datapoint[1] == '0':
                print('%s=0 is ok'%name)
            else:
                print('%s=0 is Err' % name)
            time.sleep(2)
            Datapoint = PostPropertieDatapoint(headers,server,key,'1')
            time.sleep(2)
            GropertieInfo = GetGropertieInfo(headers,key)
            if GropertieInfo[0] == '1' and Datapoint[1] == '1':
                print('%s=1 is ok'%name)
            else:
                print('%s=1 is Err' % name)

