import time
import os

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

from Routing.AutoConnWiFi import connect_wifi

def click_elenium_by_xpath(browser,path):
    for i in range(20):
       try:
            browser.find_element_by_xpath(path).click()
            return True
       except Exception as e:
           time.sleep(2)
    return False
def find_elenium_by_xpath(browser,path):
    for i in range(20):
        try:
            result = browser.find_element_by_xpath(path)
            return result
        except Exception as e:
            time.sleep(2)
    return None
def loding_display(browser,path):
    for i in range(20):
        try:
            #loading = browser.find_element_by_xpath(path)
            WebDriverWait(browser,40,1).until_not(EC.presence_of_element_located(By.XPATH,path))
            print(i)
            time.sleep(2)
        except Exception as e:
            return

def SetHUAWEI_WS(web_path,ssid,password,width,channel,ap_mode):
    web_url = "http://192.168.3.1"
    keyMaterial = "01000000D08C9DDF0115D1118C7A00C04FC297EB01000000347E492CCEF92F4B8C3D953EDD719F8000000000020000000000106600000001000020000000743E34B63E23EBF732947DFDEADDB2D8DA3EBA04057F7B89B7269FECFD28EA25000000000E80000000020000200000002F1E05CC303935F6A4379664E848123BB103A60BD5D908A4F2178026A42F5E491000000074700635BEEC7DAE9907CCDD07D95ECC40000000FDB788B0AE03D3B24D07A8A0C340FF830941987CF2F478AC686B33747EE593C8B7D90981C3C26C051E11F67E6BA9B1E0044A9D756197D7648A38503FB78A2532"
    chrome_driver = web_path
    browser = webdriver.Chrome(executable_path=chrome_driver)
    browser.get(web_url)
    time.sleep(5)
    browser.maximize_window()

    login_pwd = find_elenium_by_xpath(browser,"//*[@id=\"userpassword_ctrl\"]")#//*[@id="userpassword_ctrl"]
    if login_pwd == None:
        return
    login_pwd.click()
    login_pwd.clear()
    login_pwd.send_keys("admin123")                                           #网页后台密码
    click_elenium_by_xpath(browser,"//*[@id=\"loginbtn\"]")                   #登录
    click_elenium_by_xpath(browser,"//*[@id=\"wifi\"]")                       #点击wifi设置
    time.sleep(2)
    if ap_mode.find("wifi-") != -1:
        #设置安全加密方式
        enc = ap_mode.split("-")[-2]
        click_elenium_by_xpath(browser,"//*[@id=\"wifi_secopt2G_ctrl_selectlist_parenselect\"]")  # 加密方式下拉列表
        click_elenium_by_xpath(browser,"//*[@id=\"%s_selectlist_SmallSelectBoxScrollItemID\"]"%(enc))#选择加密方式
        time.sleep(2)

        if enc != "None":
            pwd_btn = browser.find_element_by_xpath("//*[@id=\"content_wifi_password2G_ctrl\"]")#//*[@id="content_wifi_password2G_ctrl"]
            pwd_btn.click()
            pwd_btn.clear()
            time.sleep(1)
            pwd_btn.send_keys(password)
        browser.find_element_by_xpath("//*[@id=\"SsidSettings_submitbutton\"]").click() #保存设置
        time.sleep(1)
        loding_display(browser,"//*[@id=\"loading\"]")
        #time.sleep(30)
        if enc == "None":
            for i in range(5):
                if connect_wifi(ssid,keyMaterial,sec="") == True:
                    break
            time.sleep(2)
        else:
            for i in range(5):
                if connect_wifi(ssid,keyMaterial,sec=enc) == True:
                    break
            time.sleep(2)
        browser.refresh()  # 重连wifi刷新网页

        time.sleep(2)
        #穿墙模式
        power = ap_mode.split("-")[-1]
        click_elenium_by_xpath(browser,"//*[@id=\"wifi_pwrmode_ctrl_selectlist_parenselect\"]")  # 设置信号模式(穿墙/标准/省电)//*[@id="wifi_pwrmode_ctrl_selectlist_parenselect"]
        browser.find_element_by_xpath("//*[@id=\"%s_wifi_pwrmode_ctrl_selectlist_SmallSelectBoxScrollItemID\"]"%(power)).click()
        #browser.find_element_by_xpath("//*[@id=\"wifi_pwrmode_ctrl\"]").click()#//*[@id="wifi_pwrmode_ctrl"]
        #browser.find_element_by_xpath("//*[@id=\"%s_BigSelectBoxItemID\"]"%(power)).click()
        time.sleep(2)
        if power != "02":
            browser.find_element_by_xpath("//*[@id=\"cancel\"]").click()  # //*[@id="cancel"]
            time.sleep(1)
        browser.find_element_by_xpath("//*[@id=\"pwrmode_btn\"]").click()   #保存信号强度模式
        time.sleep(1)
        loding_display(browser,"//*[@id=\"loading\"]")
        ##################################更多设置默认####################################
        click_elenium_by_xpath(browser,"//*[@id=\"more\"]")  # 更多设置
        time.sleep(2)

        click_elenium_by_xpath(browser,"//*[@id=\"wifisettingsparent_menuId\"]")#wifisettingsparent_menuId
        time.sleep(2)

        click_elenium_by_xpath(browser,"//*[@id=\"wlanadvance\"]/div[2]/ul[1]/li[1]/div[2]/div")  # //*[@id="wifi_channel24g_ctrl_selectlist_parenselect"]
        time.sleep(2)
        scroll_bar = browser.find_element_by_xpath(
            "//*[@id=\"wlanadvance\"]/div[2]/ul[1]/li[1]/div[2]/div/div[3]/div")  # //*[@id="wlanadvance"]/div[2]/ul[1]/li[1]/div[2]/div/div[3]/div

        #set_channel = browser.find_element_by_xpath("//*[@id=\"wifi_channel24g_ctrl_selectbox\"]").click()
        #time.sleep(2)
        #scroll_bar = browser.find_element_by_xpath("//*[@id=\"mCSB_1_dragger_vertical\"]")  # //*[@id="mCSB_2_dragger_vertical"]

        top_px = 0
        while True:  # 选择设置的信道
            ActionChains(browser).drag_and_drop_by_offset(scroll_bar, 0, top_px).perform()
            try:
                select_channel = browser.find_element_by_xpath(
                    "//*[@id=\"0_wifi_channel24g_ctrl_selectlist_SmallSelectBoxScrollItemID\"]").click()
                top_px = 0
                break
            except Exception as e:
                top_px += 20
                continue
        time.sleep(1)
        # 设置B/G/N模式
        browser.find_element_by_xpath(
            "//*[@id=\"wlan_mode_ctrl_selectlist_parenselect\"]").click()  # //*[@id="wlan_mode_ctrl_selectlist_parenselect"]
        time.sleep(1)
        browser.find_element_by_xpath("//*[@id=\"b/g_selectlist_SmallSelectBoxScrollItemID\"]").click()

        #browser.find_element_by_xpath("//*[@id=\"wlan_mode_ctrl_selectbox\"]").click()
        #time.sleep(1)
        #browser.find_element_by_xpath("// *[ @ id = \"b/g_BigSelectBoxItemID\"]").click()  # 选择模式//*[@id="wlan_mode_ctrl_selectbox"]
        time.sleep(2)
        #设置WMM
        browser.find_element_by_xpath(
            "//*[@id=\"wifi_wmm_enable_ctrl_selectlist_parenselect\"]").click()  # //*[@id="wifi_wmm_enable_ctrl_selectlist_parenselect"]
        time.sleep(1)
        browser.find_element_by_xpath(
            "//*[@id=\"true_wmm_enable_selectlist_SmallSelectBoxScrollItemID\"]").click()

        #browser.find_element_by_xpath("//*[@id=\"wifi_wmm_enable_ctrl_selectbox\"]").click()
        #browser.find_element_by_xpath("//*[@id=\"true_BigSelectBoxItemID\"]").click()
        time.sleep(2)
        # 保存
        browser.find_element_by_xpath("//*[@id=\"SendSettings_submitbutton\"]").click()
        loding_display(browser,"//*[@id=\"loading\"]")
    else:
        #########################################WiFi设置默认#########################################
        """"""
        click_elenium_by_xpath(browser,"//*[@id=\"wifi_secopt2G_ctrl_selectlist_parenselect\"]")  #//*[@id="wifi_secopt2G_ctrl_selectlist_parenselect"]
        click_elenium_by_xpath(browser,"//*[@id=\"11i_selectlist_SmallSelectBoxScrollItemID\"]" )#//*[@id="11i_selectlist_SmallSelectBoxScrollItemID"]
        time.sleep(2)

        browser.find_element_by_xpath("//*[@id=\"SsidSettings_submitbutton\"]").click()  # 保存设置
        time.sleep(2)
        #time.sleep(30)
        loding_display(browser,"//*[@id=\"loading\"]")
        for i in range(5):
            if connect_wifi(ssid, keyMaterial, sec="11i") == True:
                break
            time.sleep(2)

        browser.refresh()  # 重连wifi刷新网页
        time.sleep(2)
        click_elenium_by_xpath(browser,"//*[@id=\"wifi_pwrmode_ctrl_selectlist_parenselect\"]")#设置信号模式(穿墙/标准/省电)//*[@id="wifi_pwrmode_ctrl_selectlist_parenselect"]
        browser.find_element_by_xpath("//*[@id=\"02_wifi_pwrmode_ctrl_selectlist_SmallSelectBoxScrollItemID\"]" ).click()#//*[@id="00_wifi_pwrmode_ctrl_selectlist_SmallSelectBoxScrollItemID"]
        time.sleep(2)
        browser.find_element_by_xpath("//*[@id=\"pwrmode_btn\"]").click()  # 保存信号强度模式
        time.sleep(1)
        loding_display(browser,"//*[@id=\"loading\"]")
        ##########################################更多设置############################################
        click_elenium_by_xpath(browser,"//*[@id=\"more\"]")              #更多设置
        time.sleep(2)

        click_elenium_by_xpath(browser,"//*[@id=\"wifisettingsparent_menuId\"]")#//*[@id="wifisettingsparent_menuId"]
        time.sleep(5)

        set_channel = browser.find_element_by_xpath("//*[@id=\"wlanadvance\"]/div[2]/ul[1]/li[1]/div[2]/div").click()#//*[@id="wifi_channel24g_ctrl_selectlist_parenselect"]
        time.sleep(2)
        scroll_bar = browser.find_element_by_xpath("//*[@id=\"wlanadvance\"]/div[2]/ul[1]/li[1]/div[2]/div/div[3]/div")  #//*[@id="wlanadvance"]/div[2]/ul[1]/li[1]/div[2]/div/div[3]/div

        top_px = 0
        while True:     #选择设置的信道
            ActionChains(browser).drag_and_drop_by_offset(scroll_bar,0,top_px).perform()
            try:
                #//*[@id="2_wifi_channel24g_ctrl_selectlist_SmallSelectBoxScrollItemID"]
                select_channel = browser.find_element_by_xpath("//*[@id=\"%d_wifi_channel24g_ctrl_selectlist_SmallSelectBoxScrollItemID\"]"%(channel)).click()
                top_px = 0
                break
            except Exception as e:
                top_px += 20
                continue
        time.sleep(2)
        #设置B/G/N模式
        BGN_mode = ap_mode.split(",")[0]
        browser.find_element_by_xpath("//*[@id=\"wlan_mode_ctrl_selectlist_parenselect\"]").click()#//*[@id="wlan_mode_ctrl_selectlist_parenselect"]
        browser.find_element_by_xpath("//*[@id=\"%s_selectlist_SmallSelectBoxScrollItemID\"]"%(BGN_mode)).click()#选择模式//*[@id="b/g/n_selectlist_SmallSelectBoxScrollItemID"]
        time.sleep(2)

        #设置频宽
        if ap_mode.find('n') != -1:
            interval = ap_mode.split(",")[-1]
            browser.find_element_by_xpath("//*[@id=\"wifi_bind_set_ctrl_selectlist_parenselect\"]").click()#//*[@id="wifi_bind_set_ctrl_selectlist_parenselect"]
            browser.find_element_by_xpath("//*[@id=\"%s_selectlist_SmallSelectBoxScrollItemID\"]"%(width)).click()#//*[@id="20_selectlist_SmallSelectBoxScrollItemID"]
            time.sleep(2)
            #设置11n前导间隔设置
            browser.find_element_by_xpath("//*[@id=\"wlan_11ngi_ctrl_selectlist_parenselect\"]").click()#//*[@id="wlan_11ngi_ctrl_selectlist_parenselect"]
            browser.find_element_by_xpath("//*[@id=\"%s_selectlist_SmallSelectBoxScrollItemID\"]"%(interval)).click()#//*[@id="long_selectlist_SmallSelectBoxScrollItemID"]
            time.sleep(2)
        elif width.find("e") != -1:
            #设置WMM开关
            browser.find_element_by_xpath("//*[@id=\"wifi_wmm_enable_ctrl_selectlist_parenselect\"]").click()#//*[@id="wifi_wmm_enable_ctrl_selectlist_parenselect"]
            browser.find_element_by_xpath("//*[@id=\"%s_wmm_enable_selectlist_SmallSelectBoxScrollItemID\"]"%(width)).click()#//*[@id="true_wmm_enable_selectlist_SmallSelectBoxScrollItemID"]
            time.sleep(2)
        else:
            browser.find_element_by_xpath("//*[@id=\"wifi_wmm_enable_ctrl_selectlist_parenselect\"]").click()
            browser.find_element_by_xpath("//*[@id=\"true_wmm_enable_selectlist_SmallSelectBoxItemID\"]" ).click()
            time.sleep(2)
        #保存
        browser.find_element_by_xpath("//*[@id=\"SendSettings_submitbutton\"]").click()

    time.sleep(5)
    browser.close()

if __name__=="__main__":
    ssid = "Tester"
    password = "aylatest"
    width = "40"
    channel = 10
    ap_mode = ('wifi-11i-02','wifi-None-02','wifi-WPAand11i-02','wifi-11i-00','wifi-11i-01',#wifi 加密方式/WiFi功率
                                 'b/g','b/g/n,short','b/g/n,long','b','g')
    web_path = "C:\\Users\Sakura\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    for i in range(9):
        print("ap_mode = %d"%(i))
        SetHUAWEI_WS(web_path,ssid,password,width,channel,ap_mode[i])