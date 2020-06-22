import time
import os
import xlrd
import traceback

from xlutils.copy import copy
from appium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from Routing.aes_key import encrypt
from Excel.excel_rw import write_excel_by_row,get_excel_rows
from Routing.airkiss_conn import airkiss_con
from Routing.route360 import SetRoute as Set360Route
from Routing.routeMi import SetMIRoute
from Routing.FAST36E import SetRouteFAST
from Routing.CiscoRoute import SetCiscoRoute
from Routing.HUAWEI_Route import SetHUAWEI_Route
from Routing.DLinkRoute import SetRouteDLink
from Routing.NETGEAR_Route import SetRouterNETGEAR
from Routing.ASUS_Route import SetASUS_Router
from Routing.Tenda_Route import SetTenda_Route
from Routing.TP_Link_route import SetTPLinkD841Route
from Routing.TP_Link5620 import SetTPLink5620Route
from Routing.HUAWEI_WS import SetHUAWEI_WS
from Routing.AutoConnWiFi import connect_wifi

if __name__=="__main__":
    route_dict = {"360路由器":Set360Route,"2":SetMIRoute,"迅捷路由器":SetRouteFAST,"思科路由器":SetCiscoRoute,"华为路由器-A1":SetHUAWEI_Route,
                  "荣耀路由器-CD30":SetHUAWEI_Route,"荣耀路由器-CD15":SetHUAWEI_Route,"D-Link路由器":SetRouteDLink,"MERCURY路由器":SetRouterNETGEAR,
                  "ASUS路由器":SetASUS_Router,"Tenda路由器":SetTenda_Route,"TP-LinkD841路由器":SetTPLinkD841Route,"TP-Link5620路由器":SetTPLink5620Route,
                  "TP-Link5660路由器":SetTPLinkD841Route,"华为路由器-WS":SetHUAWEI_WS
                  }
    para_dict = {#参数首位为默认参数
                 "360路由器":{"ap_mode":(4,0,3),"width":(4,3,2)},                       #360路由器参数
                 "小米路由器":{},                                                        #小米路由器参数
                 # 迅捷路由器参数(ao_mode数字0为加密/（123）信号强度/（4）隔离模式)
                 "迅捷路由器":{"ap_mode":('11bg mixed','11n only','11g only','11b only','11bgn mixed',0,1,2,3,4),"width":(0,1)},
                 #思科路由器
                 "思科路由器":{"ap_mode":('bg-mixed','b-only','g-only','bg-mixed','gn-mixed&wl_nbw=20','gn-mixed&wl_nbw=0')},
                 #华为路由器-A1
                 "华为路由器-A1":{"ap_mode":('wifi-11i-2','wifi-None-2','wifi-WPAand11i-2','wifi-11i-0','wifi-11i-1',#wifi 加密方式/WiFi功率
                                 'b/g','b/g/n,short','b/g/n,long','b','g'),"width":('true','false','20','40','20_40')},
                 # 华为路由器-WS
                 "华为路由器-WS": {"ap_mode": ('wifi-11i-02', 'wifi-None-02', 'wifi-WPAand11i-02', 'wifi-11i-00', 'wifi-11i-01',  # wifi 加密方式/WiFi功率
                                 'b/g', 'b/g/n,short', 'b/g/n,long', 'b', 'g'), "width": ('true', 'false', '20', '40', '20_40')},
                 "荣耀路由器-CD30":{"ap_mode": ('wifi-11i-2', 'wifi-None-2', 'wifi-WPAand11i-2', 'wifi-11i-0', 'wifi-11i-2',  # wifi 加密方式/WiFi功率
                        'b/g', 'b/g/n,short', 'b/g/n,long', 'b', 'g'), "width": ('true', 'false', '20', '40', '20_40')},
                 "荣耀路由器-CD15":{ "ap_mode": ('wifi-11i-2', 'wifi-None-2', 'wifi-WPAand11i-2', 'wifi-11i-0', 'wifi-11i-1',  # wifi 加密方式/WiFi功率
                        'b/g', 'b/g/n,short', 'b/g/n,long', 'b', 'g'), "width": ('true', 'false', '20', '40', '20_40')},
                 #D-Link路由器
                 "D-Link路由器":{"ap_mode":("WPA2/AES-bg-20",'NONE-bg-20','WPA/AES-bg-20','WPAWPA2/AES-bg-20',
                                         "WPA2/AES-bgn-20","WPA2/AES-bgn-40","WPA2/AES-g-20","WPA2/AES-b-20")},
                 #MERCURY路由器                en -- 加密    none -- 不加密
                 "MERCURY路由器":{"ap_mode":("en-11bg mixed-自动","none-11bg mixed-自动","en-11bgn mixed-20MHz","en-11bgn mixed-20MHz",
                                          "en-11bgn mixed-自动","en-11n only-自动","en-11n only-20MHz","en-11bg mixed-20MHz",
                                          "en-11g only-20MHz","en-11b only-20MHz"),"width":('高,0','高,1','中,0','低,0')},
                 #NETGEAR路由器
                 "NETGEAR路由器":{"ap_mode":('300Mbps,WPA2-PSK','300Mbps,Disable','145Mbps,WPA2-PSK','g+and+b,WPA2-PSK','300Mbps,AUTO-PSK'),
                                  "width":(1,2,3,4)},
                 #ASUS路由器
                 "ASUS路由器":{"ap_mode":('psk2-auto','open-auto','pskpsk2-auto','psk2-off'),"width":(1,0,2)},
                 #Tenda路由器
                 "Tenda路由器":{"ap_mode":("WPA2/AES-bg-20","WPA/AES-bg-20","WPAWPA2/AES-bgn-20","WPA2/AES-bgn-20","WPA2/AES-bgn-40",
                                           "WPA2/AES-bgn-auto","WPA2/AES-b-20","WPA2/AES-g-20"),"width":("false","true")},
                 #TP-LinkD841路由器
                 "TP-LinkD841路由器":{"ap_mode":("11bg mixed-20MHz","11bgn mixed-40/20MHz自动","11bgn mixed-20MHz","11b only-20MHz",
                                             "11g only-20MHz","11n only-20MHz","11n only-40/20MHz自动")},
                 # TP-Link5620路由器
                 "TP-Link5620路由器": {"ap_mode": ("11bg mixed-20MHz", "11bgn mixed-40MHz/20MHz自动", "11bgn mixed-20MHz", "11b only-20MHz",
                                   "11g only-20MHz", "11n only-20MHz", "11n only-40MHz/20MHz自动")},
                 # TP-Link5660路由器
                 "TP-Link5660路由器": { "ap_mode": ("11bg mixed-20MHz", "11bgn mixed-40/20MHz自动", "11bgn mixed-20MHz", "11b only-20MHz",
                                   "11g only-20MHz", "11n only-20MHz", "11n only-40/20MHz自动")},
                }
    print(">>>>>>>>>>>>>>>>>>>>>>>路由器兼容性测试脚本<<<<<<<<<<<<<<<<<<<<<<<")

    #aylatest加密
    keyMaterial = "01000000D08C9DDF0115D1118C7A00C04FC297EB01000000347E492CCEF92F4B8C3D953EDD719F8000000000020000000000106600000001000020000000743E34B63E23EBF732947DFDEADDB2D8DA3EBA04057F7B89B7269FECFD28EA25000000000E80000000020000200000002F1E05CC303935F6A4379664E848123BB103A60BD5D908A4F2178026A42F5E491000000074700635BEEC7DAE9907CCDD07D95ECC40000000FDB788B0AE03D3B24D07A8A0C340FF830941987CF2F478AC686B33747EE593C8B7D90981C3C26C051E11F67E6BA9B1E0044A9D756197D7648A38503FB78A2532"
    """
    route_key = "1"
    ssid = "360WiFi-B7CF67"
    password = "aylatest"
    count = 1
    """
    test_count = input("设置单个路由测试次数:")
    count = int(input("设置单次配置配网次数:"))
    ssid = ""
    password = ""
    ap_mode = (4, 3, 0)  # 4--------WPA/WPA2-PSK AES;3---------WPA2-PSK AES;0--------无
    channel = 0  # 0~13
    width = (4, 3, 2)  # 20M-------2;40M--------3;自动-------4
    web_path = "C:\\Users\Sakura\AppData\Local\Google\Chrome\Application\chromedriver.exe"  # 浏览器绝对路径
    print(">>>>>>>>>>>>>>>>>>>>>>>开始<<<<<<<<<<<<<<<<<<<<<<<")
    base_path = os.path.dirname(__file__)  # 脚本路径
    #获取参与测试路由器
    conf_path = base_path+"/route_table.xls"        #配置文件路径
    print(conf_path)
    conf_file = xlrd.open_workbook(conf_path)
    conf_table = conf_file.sheets()[0]
    route_num = int(conf_table.nrows)
    print("路由器数量：%d"%(route_num-1))
    now_time = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    #结果路径
    reslut_path = base_path+"/result"
    if not os.path.exists(reslut_path):
        os.makedirs(reslut_path)
    reslut_path = base_path+"/result/result-%s.xls"%(now_time)
    print("结果路径: "+reslut_path)
    for i in range(1,route_num):            #遍历路由器
        print("路由器名称: "+str(conf_table.cell(i,0).value))
        print("WiFi名称: "+str(conf_table.cell(i,1).value))
        print("WiFi密码: "+str(conf_table.cell(i,2).value))
        #continue
        ssid = str(conf_table.cell(i,1).value)
        password = str(conf_table.cell(i,2).value)
        route_key = str(conf_table.cell(i,0).value)
        if ssid == "":
            print("%s:WiFi名称不能为空，进入下一个路由器测试"%(route_key))
            continue
        #os.system("netsh wlan connect name=%s" % (ssid))
        for n in range(3):
            if connect_wifi(ssid, keyMaterial, sec="11i")==True:
                break
        time.sleep(5)
        for cn in range(int(test_count)):   #每个路由器测试次数
            for sec in (para_dict[route_key]["ap_mode"]):                                                                #模式/加密方式

                if 'width' in para_dict[route_key]:
                    def_width = para_dict[route_key]["width"][0]
                else:
                    def_width = "None"
                if sec == para_dict[route_key]["ap_mode"][1]:
                    password = ""
                else:
                    password = 'aylatest'
                try:
                    print("password = "+password)
                    route_dict[route_key](web_path,ssid,password,def_width,channel,sec)           #设置路由器
                    # 保存配置，待配网结果写入excel表
                    data = {"0": "%s" % (route_key), "1": '', "2": "%s" % (str(def_width)),
                            "3": "%d" % (channel), "4": "%s" % (sec), "5": ""}
                    # 自动连接wifi
                    # 电脑重连WiFi(WiFi密码尽量不要改，加密方式改变可能导致电脑断开WiFi连接,下次循环无法设置路由)
                    for m in range(5):
                        if connect_wifi(ssid, keyMaterial, sec=password)==True:
                            break
                    """
                    data = {"0": "%s" % (route_key), "1": "%s" % (str(def_width)),
                                "2": "%d" % (channel), "3": "%s" % (sec)}
                      """
                    #write_excel_by_row(reslut_path, i-1, get_excel_rows(reslut_path, i - 1), data)
                    print(data)
                    airkiss_con(ssid,password,count,reslut_path,i-1,data)                                                        #开始配网
                    #time.sleep(5)
                except Exception as e:
                    print("%s ap_mode = %s设置/配网失败\n进入下一次设置"%(str(conf_table.cell(i,0).value),sec))
                    traceback.print_exc()
                    continue

            if 'width' in para_dict[route_key]:
                for wid in para_dict[route_key]["width"]:                                                         #设置频宽
                    try:
                        route_dict[route_key](web_path,ssid, password, wid, channel, para_dict[route_key]["ap_mode"][0])
                        # 配置写入excel表
                        data = {"0": "%s" % (route_key),"1":'', "2": "%s" % (str(wid)),
                                "3": "%d" % (channel), "4": "%s" % (str(para_dict[route_key]["ap_mode"][0])),"5":""}
                        #write_excel_by_row(reslut_path, i - 1, get_excel_rows(reslut_path, i - 1), data)
                        # 自动连接wifi
                        # 电脑重连WiFi(WiFi密码尽量不要改，加密方式改变可能导致电脑断开WiFi连接,下次循环无法设置路由)
                        for h in range(3):
                            if connect_wifi(ssid, keyMaterial, sec="11i") == True:
                                break
                        print(data)
                        #开始配网
                        airkiss_con(ssid, password, count, reslut_path, i - 1, data)
                        time.sleep(5)
                    except Exception as e:
                        print("%s width = %s 设置/配网失败\n进入下一次设置"%(str(conf_table.cell(i,0).value),wid))
                        traceback.print_exc()
                        continue
            for ch in range(14):                                                                                         #信道
                if 'width' in para_dict[route_key]:
                    def_width = para_dict[route_key]['width'][0]
                else:
                    def_width = "None"
                try:
                    route_dict[route_key](web_path,ssid, password, def_width, ch, para_dict[route_key]["ap_mode"][0])
                    # 配置写入excel表
                    data = {"0": "%s" % (route_key), "1": '', "2": "%s" % (str(def_width)),
                            "3": "%d" % (ch), "4": "%s" % (str(para_dict[route_key]["ap_mode"][0])), "5": ""}
                    #write_excel_by_row(reslut_path, i - 1, get_excel_rows(reslut_path, i - 1), data)
                    # 自动连接wifi
                    # 电脑重连WiFi(WiFi密码尽量不要改，加密方式改变可能导致电脑断开WiFi连接,下次循环无法设置路由)
                    time.sleep(5)
                    for j in range(3):
                        if connect_wifi(ssid, keyMaterial, sec="11i") == True:
                            break
                    print(data)
                    #开始配网
                    airkiss_con(ssid, password, count, reslut_path, i - 1, data)
                except Exception as e:
                    print("%s channel = %d 设置/配网失败\n进入下一次设置" % (str(conf_table.cell(i, 0).value), ch))
                    traceback.print_exc()
                    continue


