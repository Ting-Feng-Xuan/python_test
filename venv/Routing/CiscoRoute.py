
import requests

from  Routing.MD5_key import GetMD5Key

headers = {
    'Content-Type': "application/x-www-form-urlencoded;",
    }
def SetCiscoRoute(web_path,ssid,password,width,channel,ap_mode):

    login_url = "https://192.168.1.1/login.cgi"

    login_pass = GetMD5Key("aylatest")                    #加密登陆密码
    print(login_pass)
    session_id = ''
    payload = "submit_button=login&wait_time=0&enc=1&user=cisco&pwd=%s&sel_lang=EN&change_action=&gui_action=gozila_cgi&submit_type=continue"%(str(login_pass))
    #获取session_id
    while len(session_id) != 32:
        login_req = requests.post(url=login_url,headers=headers,data=payload,verify=False)
        respone_str = str(login_req.text)
        str2 = respone_str.split("session_id = \"")[-1]
        session_id = (str2[:str2.index("\"")])

    print("session_id:"+session_id)
    #拼接新headers
    headers["Referer"]="Referer: https://192.168.1.1/Wireless_Manual.asp;session_id="+session_id

    set_url = "https://192.168.1.1/apply.cgi;session_id="+session_id
    #设置参数
    payload = "submit_button=Wireless_Manual&gui_action=Apply&submit_type=&change_action=" \
              "&wl_wps_btn_index=0&wl_vap_idx=&guest_vlan_id=&nvset_cgi=wireless&wl_bss_enabled_0=1" \
              "&wl_bss_enabled_1=0&wl_bss_enabled_2=0&wl_bss_enabled_3=0&wl_closed_0=0&wl_closed_1=0" \
              "&wl_closed_2=0&wl_closed_3=0&wl_ap_isolate_0=0&wl_ap_isolate_1=0&wl_ap_isolate_2=0&" \
              "wl_ap_isolate_3=0&wl_wme_bss_disable_0=0&wl_wme_bss_disable_1=0&wl_wme_bss_disable_2=0" \
              "&wl_wme_bss_disable_3=0&wl_vlan_id_0=1&wl_vlan_id_1=1&wl_vlan_id_2=1&wl_vlan_id_3=1&vlan=1" \
              "&wl_ssid_0=%s&wl_ssid_1=ciscosb2&wl_ssid_2=ciscosb3&wl_ssid_3=ciscosb4&wl_guest_network=0" \
              "&wl_wme_apsd=off&basic_idx=0&wl_radio=1&wait_time=20&backname=&guest_ssid=&next_page=Wireless_Manual" \
              "&wlradio=on&all_page_start=&wl_net_mode=%s&wl_nbw=20&wl_channel=%d&wl_ap_mgmt_vlan_id=1" \
              "&all_page_end=&webpage_end="%(ssid,ap_mode,channel)

    set_req = requests.post(url=set_url,headers=headers,data=payload,verify=False)

    #print(set_req.text)

if  __name__=="__main__":
    ssid = "ciscosb1"
    pwd = "aylatest"
    width = 0
    channel = 1
    ap_mode = 0
    web_path = "C:\\Users\Sakura\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    SetCiscoRoute(web_path,ssid,pwd,width,channel,ap_mode)