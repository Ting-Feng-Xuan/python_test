import time
from Aylasunsea.API.Properties import GetPropertieInfo
from Aylasunsea.API.Properties import PostPropertieDatapoint
from Aylasunsea.API.login import login
from Aylasunsea.Public_Module.Time_Now import get_time_stamp
from Aylasunsea.Public_Module.write_excel import write_excel
from Aylasunsea.Public_Module.Time_Now import get_time_stamp
from Aylasunsea.Public_Module.Time_Now import get_TimeZone

# 以当前时间为属性A的值
# 以一定时间间隔发送属性A的值
# 获取属性A在云端更新的时间
# 设备端设置属性A的值变化时通过属性B上报相同的值
# 获取属性B在云端更新的时间
# 把获取到的所有数据保存在
if __name__ == '__main__':

    # 输入设备所在的域的oem_id
    oem_id = '7734c0fa'
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

    path = "date.csv"
    # print('1、以当前时间为属性A的值')
    # print('2、以一定时间间隔发送属性A的值')
    # print('3、获取属性A在云端更新的时间')
    # print('4、设备端设置属性A的值变化时通过属性B上报相同的值')
    # print('5、获取属性B在云端更新的时间')
    # print('6、把获取到的所有数据保存在')
    username = "guyisheng@sunseaaiot.com"
    password = "Hsxy1008"
    DSN = 'SC000W000122378'  # 需要控制设备的DSN
    Property_name = 'cmd'
    Property_name2 = 'log'


    j=1
    k = 1
    T0 = time.time()
    print("=========== 第 %d 次登陆 ============" %j)
    headers = login(url, username, password)

    # 获取时区
    timezone = get_TimeZone(headers, server, DSN)
    TimeZone = int(timezone[0:3])


    for i in range(999999999999999):
        i=i+1
        print(">>>>>>>>>> 第 %d 次循环 <<<<<<<<<<" %i)
        T = time.time()

        while T>1574997000 and T<1574997060 :

            print("-------- 第 %d 次登陆，第 %d 次循环，第 %d 次发送数据 --------" %(j,i,k,))
            k= k+1
            now_time = get_time_stamp()

            result_1 = PostPropertieDatapoint(headers,server,TimeZone,"1554446",now_time)
            result1_1 = PostPropertieDatapoint(headers,server,TimeZone,"75319",now_time)
            time.sleep(2)
            result_2 = GetPropertieInfo(headers,server,TimeZone,"1554455")
            result1_2 = GetPropertieInfo(headers,server,TimeZone,"75324")
            # print("cmd:%s" % get_status(headers,"75319")[-1])
            # time.sleep(2)
            # print("log:%s" % get_status(headers, "75324")[-1])
            # print(result)
            all_time = round((result_2[2] - T), 3)
            all_time1 = round((result1_2[2] - T), 3)
            write_excel(path,k,result_1[0],result_1[1],result_2[0],result_2[1],all_time,result1_1[0],result1_1[1],result1_2[0],result1_2[1],all_time1)
            time.sleep(10)
            T = time.time()

            if T - T0 > 20:
                T0 = time.time()
                print("=========== 第 %d 次登陆 ============" % j)
                headers = login(url, username, password)
                j = j + 1

        while T > 1574997120 and T < 1574997180:

            print("-------- 第 %d 次登陆，第 %d 次循环，第 %d 次发送数据 --------" % (j, i, k,))
            k = k + 1
            now_time = get_time_stamp()

            result_1 = PostPropertieDatapoint(headers, server, TimeZone, "1554446", now_time)
            result1_1 = PostPropertieDatapoint(headers, server, TimeZone, "75319", now_time)
            time.sleep(2)
            result_2 = GetPropertieInfo(headers, server, TimeZone, "1554455")
            result1_2 = GetPropertieInfo(headers, server, TimeZone, "75324")
            # print("cmd:%s" % get_status(headers,"75319")[-1])
            # time.sleep(2)
            # print("log:%s" % get_status(headers, "75324")[-1])
            # print(result)
            all_time = round((result_2[2] - T), 3)
            all_time1 = round((result1_2[2] - T), 3)
            write_excel(path, k, result_1[0], result_1[1], result_2[0], result_2[1], all_time, result1_1[0],
                        result1_1[1], result1_2[0], result1_2[1], all_time1)
            time.sleep(10)
            T = time.time()

            if T - T0 > 20:
                T0 = time.time()
                print("=========== 第 %d 次登陆 ============" % j)
                headers = login(url, username, password)
                j = j + 1


        if T-T0 >20:
            T0 = time.time()
            print("=========== 第 %d 次登陆 ============" % j)
            headers = login(url, username, password)
            j = j + 1
        if T > 1574997240:
            exit('测试时间结束')
        time.sleep(10)
