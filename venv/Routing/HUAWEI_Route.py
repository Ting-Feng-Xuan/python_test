import time
import os

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from Routing.AutoConnWiFi import connect_wifi

def SetHUAWEI_Route(web_path,ssid,password,width,channel,ap_mode):
    web_url = "http://192.168.3.1"
    keyMaterial = "01000000D08C9DDF0115D1118C7A00C04FC297EB01000000347E492CCEF92F4B8C3D953EDD719F8000000000020000000000106600000001000020000000743E34B63E23EBF732947DFDEADDB2D8DA3EBA04057F7B89B7269FECFD28EA25000000000E80000000020000200000002F1E05CC303935F6A4379664E848123BB103A60BD5D908A4F2178026A42F5E491000000074700635BEEC7DAE9907CCDD07D95ECC40000000FDB788B0AE03D3B24D07A8A0C340FF830941987CF2F478AC686B33747EE593C8B7D90981C3C26C051E11F67E6BA9B1E0044A9D756197D7648A38503FB78A2532"
    chrome_driver = web_path
    browser = webdriver.Chrome(executable_path=chrome_driver)
    browser.get(web_url)
    time.sleep(5)
    browser.maximize_window()

    login_pwd = browser.find_element_by_xpath("//*[@id=\"userpassword\"]")
    login_pwd.click()
    login_pwd.clear()
    login_pwd.send_keys("aylatest")                                           #输入密码

    browser.find_element_by_xpath("//*[@id=\"loginbtn\"]").click()          #登录
    time.sleep(3)

    browser.find_element_by_xpath("//*[@id=\"wifi\"]").click()              # wifi
    time.sleep(2)
    browser.find_element_by_xpath("//*[@id=\"wifi\"]")
    if ap_mode.find("wifi-") != -1:
        enc = ap_mode.split("-")[-2]
        browser.find_element_by_xpath("//*[@id=\"wifi_secopt2G_ctrl\"]").click()        #
        browser.find_element_by_xpath("//*[@id=\"%s_BigSelectBoxItemID\"]"%(enc)).click()
        time.sleep(2)
        if enc != "None":
            pwd_btn = browser.find_element_by_xpath("//*[@id=\"content_wifi_password2G_ctrl\"]")
            pwd_btn.click()
            pwd_btn.clear()
            pwd_btn.send_keys(password)
        browser.find_element_by_xpath("//*[@id=\"SsidSettings_submitbutton\"]").click() #保存设置
        time.sleep(30)
        if enc == "None":
            for i in range(3):
                if connect_wifi(ssid,keyMaterial,sec="") == True:
                    break
            time.sleep(2)
            #os.system("netsh wlan connect name=%s" % (ssid))
        else:
            for i in range(3):
                if connect_wifi(ssid,keyMaterial,sec=enc) == True:
                    break
            time.sleep(2)

        for i in range(2):
            browser.refresh()  # 重连wifi刷新网页
            time.sleep(1)

        time.sleep(10)
        power = ap_mode.split("-")[-1]
        browser.find_element_by_xpath("//*[@id=\"wifi_pwrmode_ctrl\"]").click()#//*[@id="wifi_pwrmode_ctrl"]
        browser.find_element_by_xpath("//*[@id=\"%s_BigSelectBoxItemID\"]"%(power)).click()
        time.sleep(2)
        if power != "2":
            browser.find_element_by_xpath("//*[@id=\"cancel\"]").click()  # //*[@id="cancel"]
            time.sleep(1)
        browser.find_element_by_xpath("//*[@id=\"pwrmode_btn\"]").click()   #保存信号强度模式
        time.sleep(10)
        ##################################更多设置默认####################################
        browser.find_element_by_xpath("//*[@id=\"more\"]").click()  # 更多设置
        time.sleep(2)

        browser.find_element_by_xpath("//*[@id=\"wifiadvancesetparent_menuId\"]").click()
        time.sleep(2)

        set_channel = browser.find_element_by_xpath("//*[@id=\"wifi_channel24g_ctrl_selectbox\"]").click()
        time.sleep(2)
        scroll_bar = browser.find_element_by_xpath(
            "//*[@id=\"mCSB_1_dragger_vertical\"]")  # //*[@id="mCSB_2_dragger_vertical"]

        top_px = 0
        while True:  # 选择设置的信道
            ActionChains(browser).drag_and_drop_by_offset(scroll_bar, 0, top_px).perform()
            try:
                select_channel = browser.find_element_by_xpath(
                    "//*[@id=\"0_BigSelectBoxScrollItemID\"]").click()
                top_px = 0
                break
            except Exception as e:
                top_px += 20
                continue
        time.sleep(1)
        # 设置B/G/N模式
        browser.find_element_by_xpath("//*[@id=\"wlan_mode_ctrl_selectbox\"]").click()
        time.sleep(1)
        browser.find_element_by_xpath("// *[ @ id = \"b/g_BigSelectBoxItemID\"]").click()  # 选择模式//*[@id="wlan_mode_ctrl_selectbox"]
        time.sleep(2)
        #设置WMM
        browser.find_element_by_xpath("//*[@id=\"wifi_wmm_enable_ctrl_selectbox\"]").click()
        browser.find_element_by_xpath("//*[@id=\"true_BigSelectBoxItemID\"]").click()
        time.sleep(2)

    else:
        #########################################WiFi设置默认#########################################
        browser.find_element_by_xpath("//*[@id=\"wifi_secopt2G_ctrl\"]").click()  #
        browser.find_element_by_xpath("//*[@id=\"11i_BigSelectBoxItemID\"]" ).click()
        time.sleep(2)

        browser.find_element_by_xpath("//*[@id=\"SsidSettings_submitbutton\"]").click()  # 保存设置
        time.sleep(30)

        connect_wifi(ssid, keyMaterial, sec="11i")
        time.sleep(2)
        for i in range(5):
            browser.refresh()  # 重连wifi刷新网页
            time.sleep(2)
        time.sleep(10)
        browser.find_element_by_xpath("//*[@id=\"wifi_pwrmode_ctrl\"]").click()#设置信号模式(穿墙/标准/省电)
        browser.find_element_by_xpath("//*[@id=\"2_BigSelectBoxItemID\"]" ).click()
        time.sleep(2)

        browser.find_element_by_xpath("//*[@id=\"pwrmode_btn\"]").click()  # 保存信号强度模式
        time.sleep(10)
        ##########################################更多设置############################################
        browser.find_element_by_xpath("//*[@id=\"more\"]").click()              #更多设置
        time.sleep(2)

        browser.find_element_by_xpath("//*[@id=\"wifiadvancesetparent_menuId\"]").click()
        time.sleep(2)

        set_channel = browser.find_element_by_xpath("//*[@id=\"wifi_channel24g_ctrl_selectbox\"]").click()
        time.sleep(2)
        scroll_bar = browser.find_element_by_xpath("//*[@id=\"mCSB_1_dragger_vertical\"]")        #//*[@id="mCSB_2_dragger_vertical"]

        top_px = 0
        while True:     #选择设置的信道
            ActionChains(browser).drag_and_drop_by_offset(scroll_bar,0,top_px).perform()
            try:
                select_channel = browser.find_element_by_xpath("//*[@id=\"%d_BigSelectBoxScrollItemID\"]"%(channel)).click()
                top_px = 0
                break
            except Exception as e:
                top_px += 20
                continue
        time.sleep(2)
        #设置B/G/N模式
        BGN_mode = ap_mode.split(",")[0]
        browser.find_element_by_xpath("//*[@id=\"wlan_mode_ctrl_selectbox\"]").click()
        browser.find_element_by_xpath("// *[ @ id = \"%s_BigSelectBoxItemID\"]"%(BGN_mode)).click()#选择模式//*[@id="wlan_mode_ctrl_selectbox"]
        time.sleep(2)

        #设置频宽
        if ap_mode.find('n') != -1:
            interval = ap_mode.split(",")[-1]
            browser.find_element_by_xpath("//*[@id=\"wifi_bind_set_ctrl_selectlist_childselect\"]").click()
            browser.find_element_by_xpath("//*[@id=\"%s_BigSelectBoxItemID\"]"%(width)).click()
            time.sleep(2)
            #设置11n前导间隔设置
            browser.find_element_by_xpath("//*[@id=\"wlan_11ngi_ctrl_selectbox\"]").click()
            browser.find_element_by_xpath("//*[@id=\"%s_BigSelectBoxItemID\"]"%(interval)).click()
            time.sleep(2)
        elif width.find("e") != -1:
            #设置WMM开关
            browser.find_element_by_xpath("//*[@id=\"wifi_wmm_enable_ctrl_selectbox\"]").click()
            browser.find_element_by_xpath("//*[@id=\"%s_BigSelectBoxItemID\"]"%(width)).click()
            time.sleep(2)
        else:
            browser.find_element_by_xpath("//*[@id=\"wifi_wmm_enable_ctrl_selectbox\"]").click()
            browser.find_element_by_xpath("//*[@id=\"true_BigSelectBoxItemID\"]" ).click()
            time.sleep(2)
        #保存
        browser.find_element_by_xpath("//*[@id=\"SendSettings_submitbutton\"]").click()
        time.sleep(5)

if __name__=="__main__":
    ssid = "HUAWEI-9QVXGC"
    password = "aylatest"
    width = "40"
    channel = 6
    ap_mode = "b/g/n,short"
    web_path = "C:\\Users\Sakura\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    SetHUAWEI_Route(web_path,ssid,password,width,channel,ap_mode)