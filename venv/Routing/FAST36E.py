import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select

def SetRouteFAST(web_path,ssid,password,width,channel,ap_mode):

    web_url = "http://falogin.cn"
    chrome_driver = web_path
    browser = webdriver.Chrome(executable_path=chrome_driver)
    def_bgn = "11bg mixed"

    browser.get(web_url)
    time.sleep(3)
    login_pwd = browser.find_element_by_xpath("//*[@id=\"lgPwd\"]")
    login_pwd.click()
    login_pwd.clear()
    login_pwd.send_keys("aylatest")
    browser.find_element_by_xpath("//*[@id=\"loginSub\"]/i").click()            #登陆路由器网页
    time.sleep(2)

    browser.find_element_by_xpath("//*[@id=\"headFunc\"]/li[2]/span").click()           #高级设置
    time.sleep(2)
    wifi_menu = browser.find_element_by_xpath("//*[@id=\"wifiSet_menu\"]/label")             #无线设置//*[@id="wifiSet_menu"]/label

    wifi_menu.click()
    time.sleep(1)
     #设置无线名称
    wifi_ssid = browser.find_element_by_xpath("//*[@id=\"ssid\"]")
    wifi_ssid.click()
    wifi_ssid.clear()
    wifi_ssid.send_keys(ssid)
    #设置密码
    if password =="":
            browser.find_element_by_xpath("//*[@id=\"securityDisable\"]").click()            #不加密
    else:
            wifi_pwd = browser.find_element_by_xpath("//*[@id=\"wlanPwd\"]")
            wifi_pwd.click()
            wifi_pwd.clear()
            wifi_pwd.send_keys(password)
    #设置信道

    wifi_channel = browser.find_element_by_xpath("//*[@id=\"channel\"]/span").click()
    time.sleep(1)
    select_channel = browser.find_element_by_xpath("//*[@id=\"selOptsUlchannel\"]/li[%d]"%(channel+1)).click()

    #设置ap_mode模式
    wifi_bgn_mode = browser.find_element_by_xpath("//*[@id=\"wlanMode\"]/span")

    wifi_strength = browser.find_element_by_xpath("//*[@id=\"hcCo\"]/div[3]/ul[6]/li/span")

    wifi_pass = browser.find_element_by_xpath("//*[@id=\"securityDisable\"]")
    wifi_isolation = browser.find_element_by_xpath("//*[@id=\"apIsolate\"]")
    #设置bgn模式
    if isinstance(ap_mode,str):
        if wifi_isolation.is_selected():                                                            #默认不隔离
            wifi_isolation.click()
        if wifi_pass.is_selected():                                                                 #默认加密
             wifi_pass.click()
        wifi_strength.click()
        time.sleep(1)
        browser.find_element_by_xpath("//*[@id=\"selOptsUlwlanPower\"]/li[1]").click()              #默认信号强度
        wifi_bgn_mode.click()
        time.sleep(1)
        browser.find_element_by_xpath("//*[@id=\"selOptsUlwlanMode\"]/li[@title=\"%s\"]"%(ap_mode)).click()#设置bgn模式
    #设置不加密
    elif ap_mode == 0:
        wifi_strength.click()
        time.sleep(1)
        browser.find_element_by_xpath("//*[@id=\"selOptsUlwlanPower\"]/li[1]").click()  # 默认信号强度
        if wifi_isolation.is_selected():                        #默认不隔离
            wifi_isolation.click()
        if not wifi_pass.is_selected():                         #设置不加密
             wifi_pass.click()
        wifi_bgn_mode.click()
        time.sleep(1)
        browser.find_element_by_xpath("//*[@id=\"selOptsUlwlanMode\"]/li[@title=\"%s\"]" % ("11bg mixed")).click()  # 默认bgn模式
    #设置隔离模式
    elif ap_mode == 4:
        wifi_bgn_mode.click()
        time.sleep(1)
        browser.find_element_by_xpath( "//*[@id=\"selOptsUlwlanMode\"]/li[@title=\"%s\"]" % ("11bg mixed")).click()  # 默认bgn模式
        wifi_strength.click()
        time.sleep(1)
        browser.find_element_by_xpath("//*[@id=\"selOptsUlwlanPower\"]/li[1]").click()  # 默认信号强度
        if wifi_pass.is_selected():                         #默认加密
            wifi_pass.click()
        if not wifi_isolation.is_selected():                #设置隔离模式
            wifi_isolation.click()
        #设置信号强度
    else:
        wifi_bgn_mode.click()
        time.sleep(1)
        browser.find_element_by_xpath(
            "//*[@id=\"selOptsUlwlanMode\"]/li[@title=\"%s\"]" % ("11bg mixed")).click()  # 默认bgn模式
        wifi_strength.click()
        time.sleep(1)
        browser.find_element_by_xpath("//*[@id=\"selOptsUlwlanPower\"]/li[%d]"%(ap_mode)).click()   #设置信号强度

        if wifi_pass.is_selected():             #默认加密
             wifi_pass.click()
        if wifi_isolation.is_selected():  # 默认不隔离
            wifi_isolation.click()
    print("设置成功")

    browser.find_element_by_xpath("//*[@id=\"save\"]").click()
    time.sleep(10)
    browser.close()


if __name__=="__main__":
    ssid = "FAST_C36E"
    password = "aylatest"
    width = 4
    channel = 2
    #ap_mode = 1
    ap_mode ="11bg mixed"
    web_path = "C:\\Users\Sakura\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    SetRouteFAST(web_path,ssid,password,width,channel,ap_mode)
