import serial
import time
import datetime
import os
import xlrd
import Excel.excel_rw

from appium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

# OPPO A5
desired_caps = {
    'platformName': 'Android',
    #'platformVersion': '8.1.0',
    'platformVersion': '9',
    #'platformVersion': '5.1.1',
    'appPackage': 'com.sunseaaiot.app.lark',
    'appActivity': 'com.sunseaiot.larkapp.refactor.login.SplashActivity',
    'noReset': True,  # 设置不重装app
    'deviceName': 'MI 8',
    #'unid':'61b32542',
    'resetKeyboard': True,  # 运行完成后重置软键盘的状态　　
}
#获取手机屏幕大小
def getSize(dr):
      x = dr.get_window_size()['width']
      y = dr.get_window_size()['height']
      return (x, y)
def swipeUp(dr,t):
     l = getSize(dr)
     x1 = int(l[0] * 0.5)  #x坐标
     y1 = int(l[1] * 0.75)   #起始y坐标
     y2 = int(l[1] * 0.25)   #终点y坐标
     dr.swipe(x1, y1, x1, y2,t)
def send_command(ser):
    factory = "reset factory\n\r"
    # factory = "ayla reset factory\n\r"
    ser.write(factory.encode())
    time.sleep(2)

def find_element_until_visibility(driver, locator, timeout=10):
    ele = WebDriverWait(driver, timeout).until(EC.visibility_of_any_elements_located((By.ID, locator)))
    return ele
def find_end_buton(driver,id_path,timeout):
    while timeout > 0:
        try:
            finish_button = driver.find_element_by_id(id_path)
            return finish_button
            break
        except Exception as e:
            timeout -= 1
            time.sleep(1)
    return False
def click_element_by_xpath(driver,path):
    for i in range(10):
        try:
            driver.find_element_by_xpath(path).click()
            break
        except Exception as e:
            time.sleep(1)
def click_element_by_id(driver,path):
    for i in range(10):
        try:
            driver.find_element_by_id(path).click()
            break
        except Exception as e:
            time.sleep(1)

# 判断元素是否存在
def isElement(driver, ele, timeout=5):
    Flag = None
    try:
        driver.find_element_by_id(ele)
        Flag = True
    except NoSuchElementException:
        Flag = False
    finally:
        return Flag

#if __name__ == '__main__':
# wifi_ssid: wifi名称
# wifi_psd:  wifi密码
# num: 路由器存放结果工作表,例 sheet1为0
# result_path:存放结果文件的路径
def airkiss_con(wifi_ssid,wifi_psd,count,result_path,num,data):
    base_path = os.path.dirname(__file__)  # 获取当前脚本的绝对路径



    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    #wifi = "test6"                                                         # 指定要连接的WiFi
    wifi = wifi_ssid
    # wifi = "TP-LINK_Tester"
    #wifi_pwd = "test12345"                                                       # WiFi密码
    wifi_pwd = wifi_psd
    result_file = os.path.join(base_path, "Wifi_join.txt")                       # 存储配网情况的文件
    log_file = os.path.join(base_path, "Log.txt")  # 配网日志
    success_time = 0                                                             # 统计成功的次数
    fail_time = 0                                                                # 统计失败的次数
    #cycle_time = 100                                                             # 循环次数
    cycle_time = count
    done_time = 0                                                               # 已执行次数,默认是0,具体根据实际情况来
    # 登录App,可以跳过次步骤
    # username = "2212249179@qq.com"
    # password = "123456"
    # driver.find_element_by_id('userNameEditText').clear()
    # driver.find_element_by_id('userNameEditText').send_keys(username)          # 用户名
    # driver.find_element_by_id('passwordEditText').clear()
    # driver.find_element_by_id('passwordEditText').send_keys(password)          # 密码
    # # driver.keyevent(4)                                                       # 收回键盘
    # driver.find_element_by_id('buttonSignIn').click()
    for i in range(cycle_time):
        # 设备配网
        k = done_time + i + 1
        conn_time = datetime.datetime.now()
        print("第%s次配网开始时间:%s" % (i+1, conn_time))
        time.sleep(3)
        driver.wait_activity(".MainActivity",10)
        click_element_by_id(driver,"com.sunseaaiot.app.lark:id/add_device")                           # 添加设备按钮

        ser = serial.Serial('COM9', 115200, timeout=3)  # 串口工具初始化,串口的端口需要根据实际情况更改
        send_command(ser)        # 通过串口下发指令
        ser.close()

        time.sleep(3)
        send_time = datetime.datetime.now()
        click_element_by_xpath(driver,"//android.widget.TextView[@text='插座']")                   # 点击"插座"按钮

        time.sleep(2)
        click_element_by_id(driver,"com.sunseaaiot.app.lark:id/ck_how_to_config")               #确认快闪操作

        time.sleep(1)
        click_element_by_id(driver,"com.sunseaaiot.app.lark:id/btn_bottom")

        time.sleep(2)
        #wifi_filed = find_element_until_visibility("com.sunseaaiot.app.lark:id/tv_wifi_ssid")          # 获取当前连接的WiFi
        wifi_filed = driver.find_element_by_id("com.sunseaaiot.app.lark:id/tv_wifi_ssid")
        wifi_name = wifi_filed.text
        print(wifi_name)
        # 异常处理,连接的WiFi不是指定的WiFi需切换
        if wifi_name != wifi:
            change_btn = driver.find_element_by_id("com.sunseaaiot.app.lark:id/tv_change_network")         # 切换网络按钮
            change_btn.click()
            #ss_wifi = driver.find_element_by_xpath("//android.widget.TextView[@text='{wifi}']".format(wifi=wifi))       # 选择指定的WiFi
            time.sleep(2)
            while True:
                try:
                    click_element_by_xpath(driver,"//android.widget.LinearLayout[contains(@content-desc,'{wifi}')]".format(wifi=wifi))
                    time.sleep(1)
                    click_wifi = driver.find_element_by_id("com.android.settings:id/title")
                    if click_wifi.text != wifi:
                        #driver.find_element_by_id("android:id/button3").click()
                        time.sleep(1)
                        continue
                    #driver.find_element_by_id("android:id/button1").click()
                    time.sleep(3)
                    driver.keyevent(4)
                    #driver.find_element_by_xpath("//android.widget.ImageView[@content-desc=\"返回\"]").click()
                    time.sleep(3)
                    break
                except Exception as e:
                    time.sleep(1)
                    #swipeUp(driver,10)

        wifi_pass = driver.find_element_by_id("com.sunseaaiot.app.lark:id/et_wifi_password")
        wifi_pass.clear()
        if wifi_pwd == "":
            time.sleep(1)
            driver.find_element_by_id("com.sunseaaiot.app.lark:id/tv_next").click()                         #无密码配网，直接点击下一步
            time.sleep(1)
            driver.find_element_by_id("com.sunseaaiot.app.lark:id/tv_common_define").click()
            #click_element_by_id(driver,"com.sunseaaiot.app.lark:id/tv_common_define")
        else:
            wifi_pass.send_keys(wifi_pwd)
            driver.find_element_by_id("com.sunseaaiot.app.lark:id/tv_next").click()                            # 点击下一步按钮
        d1 = datetime.datetime.now()                                                                           # 开始时间
        time.sleep(3)
        #finish_btn = find_element_until_visibility(driver,"com.sunseaaiot.app.lark:id/btn_bottom", timeout=240)      # 配网完成会出现一个button
        finish_btn = find_end_buton(driver, "com.sunseaaiot.app.lark:id/btn_bottom", 200)
        d2 = datetime.datetime.now()                                                                        # 结束时间

        text = finish_btn.text
        print(text)
        # 获取配网结束后的button上的文本
        # 根据button上的文本判断配网是否成功
        if text == "完成":
            result = "Pass"
            success_time = success_time + 1
        else:
            result = "Failed"
            fail_time = fail_time + 1
        cost_time = (d2-d1).seconds
        time.sleep(3)
        # 统计配网情况
        with open(result_file, 'a+') as f:
            f.write("时间{conn_time}!第{i}次配网情况:{result},耗时:{cost_time}s\n".format(conn_time=conn_time, i=k, result=result, cost_time=cost_time))
        #结果写入excel表
        data["1"] = "第%d次"%(k)
        data["5"] = result
        Excel.excel_rw.write_excel_by_row(result_path,num,Excel.excel_rw.get_excel_rows(result_path,num),data)
            # 配网日志
        with open(log_file, 'a+') as h:
                h.write("第{i}次配网!配网开始时间:{conn_time}    配网结束时间:{finish_time}    设备reset factory:{send_time}\n".format(i=k,
                                                                                                                 conn_time=conn_time,
                                                                                                                 finish_time=d2,
                                                                                                                 send_time=send_time))
        # 异常处理,不管设备配网成功与否,点击4次返回按键回主菜单,并重启App
        for i in range(5):
            driver.keyevent(4)
            time.sleep(1)
        time.sleep(3)
    driver.close()
    with open(result_file, 'a+') as f:
        f.write("总体配网情况:成功{success_time}次,失败{fail_time}次\n".format(success_time=success_time, fail_time=fail_time))
"""
    # ======================分割线,以下是App先进入配网模式,设备延时20s======================
    test_file = os.path.join(base_path, "Wifi_join_app.txt")  # 用于存储App先进入配网模式的日志
    success_time = 0  # 统计成功的次数
    fail_time = 0  # 统计失败的次数
    cycle_time1 = 100
    done_time1 = 0
    for i in range(cycle_time1):
        # 设备配网
        k = done_time1 + i + 1
        conn_time = datetime.datetime.now()
        print("第%s次配网开始时间:%s" % (i+1, conn_time))
        time.sleep(3)
        driver.wait_activity(".MainActivity",20)
        add_btn = driver.find_element_by_id("com.sunseaaiot.app.lark:id/add_device")                                                     # 添加设备按钮
        add_btn.click()
        send_command(ser)        # 通过串口下发指令
        send_time = datetime.datetime.now()
        btn_bottom = driver.find_element_by_xpath("//android.widget.TextView[@text='插座']")                   # 点击"插座"按钮
        btn_bottom.click()
        time.sleep(2)
        confirm_check = driver.find_element_by_id("com.sunseaaiot.app.lark:id/ck_how_to_config")                # 确认快闪操作
        confirm_check.click()
        time.sleep(1)
        btn_next = driver.find_element_by_id("com.sunseaaiot.app.lark:id/btn_bottom")
        btn_next.click()
        time.sleep(1)   
        wifi_filed = find_element_until_visibility(driver, "com.sunseaaiot.app.lark:id/tv_wifi_ssid")          # 获取当前连接的WiFi
        wifi_name = wifi_filed[0].text
        # 异常处理,连接的WiFi不是指定的WiFi需切换
        if wifi_name != wifi:
            change_btn = driver.find_element_by_id("com.sunseaaiot.app.lark:id/tv_change_network")         # 切换网络按钮
            change_btn.click()
            time.sleep(2)
            ss_wifi = driver.find_element_by_xpath("//android.widget.TextView[@text='{wifi}']".format(wifi=wifi))       # 选择指定的WiFi
            ss_wifi.click()
            driver.keyevent(4)
        driver.find_element_by_id("com.sunseaaiot.app.lark:id/tv_next").click()                            # 点击下一步按钮
        d1 = datetime.datetime.now()                                                                       # 开始时间
        time.sleep(20)
        send_command(ser)                                                                                   # 下发指令到设备
        send_time = datetime.datetime.now()
        finish_btn = find_element_until_visibility(driver,"com.sunseaaiot.app.lark:id/btn_bottom", 240)      # 配网完成会出现一个button
        d2 = datetime.datetime.now()                                                                        # 结束时间
        text = finish_btn[0].text                                                                           # 获取配网结束后的button上的文本
        # 根据button上的文本判断配网是否成功
        if text == "完成":
            result = "Success"
            success_time = success_time + 1
        else:
            result = "Failed"
            fail_time = fail_time + 1
        cost_time = (d2-d1).seconds
        time.sleep(3)
        # 统计配网情况
        with open(test_file, 'a+') as f:
            f.write("时间{conn_time}!第{i}次配网情况:{result},耗时:{cost_time}s\n".format(conn_time=conn_time, i=k, result=result, cost_time=cost_time))
            # 配网日志
        with open(log_file, 'a+') as h:
                h.write("第{i}次配网!配网开始时间:{conn_time}    配网结束时间:{finish_time}    设备reset factory:{send_time}\n".format(i=k,
                                                                                                                 conn_time=conn_time,
                                                                                                                 finish_time=d2,
                                                                                                                 send_time=send_time))
        # 异常处理,不管设备配网成功与否,点击4次返回按键回主菜单,并重启App
        for i in range(4):
            driver.keyevent(4)
            time.sleep(1)
        time.sleep(3)

    with open(test_file, 'a+') as f:
        f.write("总体配网情况:成功{success_time}次,失败{fail_time}次\n".format(success_time=success_time, fail_time=fail_time))
"""
if __name__=="__main__":
    wifi_ssid = "ASUS"
    wifi_pwd = ""
    count = 3
    num = 1
    data = {"0": "ASUS" , "1": '', "2": "0",
            "3": "1", "4": "11", "5": ""}
    result_path = "D:/py/venv/Routing/result/result-2019-12-25-17-52-40.xls"
    #wifi_ssid,wifi_psd,count,result_path,num
    airkiss_con(wifi_ssid,wifi_pwd,count,result_path,num,data)