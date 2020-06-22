import time
import os

from selenium import webdriver

def SetMERCURY_Route(web_path,ssid,password,width,channel,ap_mode):
    web_url = "http://melogin.cn/"

    chrome_driver = web_path
    browser = webdriver.Chrome(executable_path=chrome_driver)
    browser.get(web_url)
    time.sleep(5)
    browser.maximize_window()
    time.sleep(1)

    sec = ap_mode.split('-')[0]
    bgn_mode = ap_mode.split('-')[1]
    wifi_width = ap_mode.split('-')[-1]
    browser.find_element_by_xpath("//*[@id=\"lgPwd\"]").send_keys("aylatest")
    browser.find_element_by_xpath("//*[@id=\"loginSub\"]/i").click()            #登陆
    time.sleep(3)

    browser.find_element_by_xpath("//*[@id=\"headFunc\"]/li[2]/span").click()
    time.sleep(2)
    browser.find_element_by_xpath("//*[@id=\"wifiSet_menu\"]").click()
    time.sleep(1)
    #设置密码
    if sec=="none":
        browser.find_element_by_xpath("//*[@id=\"securityDisable\"]").click()
    else:
        wifi_pwd = browser.find_element_by_xpath("//*[@id=\"wlanPwd\"]")
        wifi_pwd.click()
        wifi_pwd.clear()
        wifi_pwd.send_keys(password)
     #设置信道

    browser.find_element_by_class_name("highSetSelect").click()
    time.sleep(1)
    browser.find_element_by_xpath("//*[@id=\"selOptsUlchannel\"]/li[%d]"%(channel+1)).click()
    time.sleep(2)

    #设置BGN模式
    browser.find_element_by_xpath("//*[@id=\"wlanMode\"]").click()
    time.sleep(1)
    browser.find_element_by_xpath("//*[@title=\"%s\"]"%(bgn_mode)).click()
    time.sleep(2)

    #设置带宽
    if bgn_mode.find("n ") != -1:
        browser.find_element_by_xpath("//*[@id=\"wlanWidth\"]").click()
        time.sleep(1)
        browser.find_element_by_xpath("//*[@title=\"%s\"]"%(wifi_width)).click()
        time.sleep(2)

    strength = width.split(',')[0]
    ap_isolation = width.split(',')[-1]
    #设置信号强度
    browser.find_element_by_xpath("//*[@id=\"wlanPower\"]").click()
    time.sleep(1)
    browser.find_element_by_xpath("//*[@title=\"%s\"]"%(strength)).click()
    time.sleep(2)
    if ap_isolation == "1":
        browser.find_element_by_xpath("//*[@id=\"apIsolate\"]").click()

    browser.find_element_by_xpath("//*[@id=\"save\"]/i")                        #保存
    time.sleep(5)

if __name__ =="__main__":
    ssid = "MERCURY_CCC4"
    password = "aylatest"
    width = "中,1"
    channel = 6
    ap_mode = "none-11bgn mixed-20MHz"
    web_path = "C:\\Users\Sakura\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    SetMERCURY_Route(web_path,ssid,password,width,channel,ap_mode)