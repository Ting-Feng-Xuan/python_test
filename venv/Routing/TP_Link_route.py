import time


from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
def click_elenium_by_xpath(browser,path):
    for i in range(40):
       try:
            browser.find_element_by_xpath(path).click()
            return True
       except Exception as e:
           time.sleep(1)
    return False
def find_elenium_by_xpath(browser,path):
    for i in range(40):
        try:
            result = browser.find_element_by_xpath(path)
            return result
        except Exception as e:
            time.sleep(1)
    return None
def SetTPLinkD841Route(web_path,ssid,pwd,width,channel,ap_mode):
    web_url = "http://tplogin.cn"
    #browser = webdriver.Chrome( web_path)
    web_path = "C:\Program Files\mozilla firefox\geckodriver.exe"
    browser = webdriver.Firefox(executable_path=web_path)
    browser.get(web_url)
    time.sleep(5)
    browser.maximize_window()

    click_elenium_by_xpath(browser,"//*[@id=\"lgPwd\"]")
    browser.find_element_by_xpath("//*[@id=\"lgPwd\"]").send_keys("aylatest")
    time.sleep(1)
    browser.find_element_by_xpath("//*[@id=\"loginSub\"]").click()
    for i in range(3):
        click_elenium_by_xpath(browser,"//*[@id=\"routerSetMbtn\"]")
        time.sleep(2)
        try:
            browser.find_element_by_xpath("//*[@id=\"wireless2G_rsMenu\"]/label").click()  # 无线设置
            time.sleep(2)
            wifi_pwd = browser.find_element_by_xpath("//*[@id=\"wlanPwd\"]")
            wifi_pwd.click()
            wifi_pwd.clear()
            if pwd != "":
                wifi_pwd.send_keys(pwd)  # 设置密码
            break
        except Exception as e:
            time.sleep(2)
    # 设置信道
    browser.find_element_by_xpath("//*[@id=\"channel\"]").click()
    time.sleep(1)
    channel_bar = browser.find_element_by_xpath("/html/body/div[12]/label")#/html/body/div[12]/label
    channel_menu = browser.find_element_by_xpath("//*[@id=\"selOptsUlchannel\"]")#/html/body/div[3]/div[2]/div[1]/div[3]/div[2]/div/div/div[3]/ul[4]/li/span/span
    bar = browser.find_element_by_xpath("/html/body/div[9]/label")#//*[@id="routeSetLMenuConniceScrollSb1576805793013"]/label
    top_px = 2.68908
    #print(str(channel_menu.text))

    while True:
        #ActionChains(browser).drag_and_drop_by_offset(bar,0,top_px).perform()
        try:
            browser.find_element_by_xpath("//*[@id=\"selOptsUlchannel\"]/li[%d]" % (channel+1)).click()
            top_px = 0
            break
        except Exception as e:
            top_px += 21.5162
            ActionChains(browser).drag_and_drop_by_offset(channel_bar, 0, top_px).perform()
            ActionChains(browser).move_to_element(channel_menu).perform()
            continue
    time.sleep(2)
    #设置BGN模式
    bgn_mode = ap_mode.split('-')[0]
    browser.find_element_by_xpath("//*[@id=\"wlanMode\"]").click()
    time.sleep(1)
    browser.find_element_by_xpath("//*[@title=\"%s\"]"%(bgn_mode)).click()
    time.sleep(2)

    set_width = ap_mode.split('-')[-1]
    #设置频宽
    if ap_mode.find('n ') != -1:
        browser.find_element_by_xpath("//*[@id=\"wlanWidth\"]").click()
        time.sleep(1)
        browser.find_element_by_xpath("//*[@title=\"%s\"]"%(set_width)).click()
        time.sleep(2)

    browser.find_element_by_xpath("//*[@id=\"save\"]").click()     #保存//*[@id="save"]
    time.sleep(5)
    browser.close()

if __name__ == "__main__":
    ssid = "TP-LINK_D841"
    pwd = "aylatest"
    width = "20MHz"
    channel = 9
    ap_mode = ("11bg mixed-20MHz","11bgn mixed-40/20MHz自动","11bgn mixed-20MHz","11b only-20MHz",
                                             "11g only-20MHz","11n only-20MHz","11n only-40/20MHz自动")
    #web_path = "C:\\Users\Sakura\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    web_path = "C:\Program Files\mozilla firefox\geckodriver.exe"
    for i in range(7):
        print(i)
        SetTPLinkD841Route(web_path,ssid,pwd,width,channel,ap_mode[i])
        time.sleep(5)