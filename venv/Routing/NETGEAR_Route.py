import requests
import time

def SetRouterNETGEAR(web_path,ssid,pwd,width,channel,ap_mode):
    id_url =  "http://www.routerlogin.net/WLG_wireless_dual_band_r10.htm"
    headers = {
        'Authorization': "Basic YWRtaW46YXlsYXRlc3Q=,Basic YWRtaW46YXlsYXRlc3Q=",

    }
    proxies = {
        "Username":"admin",
        "Password":"aylatest",
    }

    get_id = ""
    while get_id.find("wireless.cgi") == -1:
        id_req = requests.get(url=id_url, headers=headers, proxies=proxies)
        get_id = str(id_req.text).split('action=\"')[-1].split('\"')[0]

    query_id = get_id.split('id=')[-1]
    set_url = "http://www.routerlogin.net/wireless.cgi"
    querystring = {"id": query_id}
    bgn_mode = ap_mode.split(',')[0]
    sec = ap_mode.split(',')[-1]

    print(querystring)
    payload = "Apply=%%E5%%BA%%94%%E7%%94%%A8&WRegion=2&ssid_bc=ssid_24G_bc&enable_coexistence=enable_coexistence&" \
              "ssid=NETGEAR39&w_channel=%d&opmode=%s&enable_tpc=%d&security_type=%s&authAlgm=automatic&" \
              "wepenc=1&wep_key_no=1&KEY1=&KEY2=&KEY3=&KEY4=&passphrase=%s&encryptmode=1&wpa_en_gk_int=3600&" \
              "RADIUSAddr1_wla=&RADIUSAddr2_wla=&RADIUSAddr3_wla=&RADIUSAddr4_wla=&wpa_en_radius_port=1812&wpa_en_radius_ss=&" \
              "ssid_an=NETGEAR39-5G&w_channel_an=153&opmode_an=HT80&enable_tpc_an=1&security_type_an=WPA2-PSK&" \
              "authAlgm_an=automatic&wepenc_an=1&wep_key_no_an=1&KEY1_an=&KEY2_an=&KEY3_an=&KEY4_an=&passphrase_an=luckycheese658&" \
              "encryptmode_an=1&wpa_en_gk_int_wlg=3600&RADIUSAddr1_wlg=&RADIUSAddr2_wlg=&RADIUSAddr3_wlg=&RADIUSAddr4_wlg=&" \
              "wpa_en_radius_port_wlg=1812&wpa_en_radius_ss_wlg=&tempSetting=0&tempRegion=5&setRegion=2&wds_enable=0&" \
              "wds_enable_an=0&only_mode=0&show_wps_alert=0&security_type_2G=WPA2-PSK&security_type_5G=WPA2-PSK&" \
              "gui_security_type_5G=&init_security_type_2G=WPA2-PSK&init_security_type_5G=WPA2-PSK&initChannel=0&" \
              "initAuthType=automatic&initDefaultKey=0&initChannel_an=153&initAuthType_an=automatic&initDefaultKey_an=0&" \
              "telec_dfs_ch_enable=1&ce_dfs_ch_enable=1&fcc_dfs_ch_enable=0&auto_channel_5G=1&support_ac_mode=1&" \
              "board_id=U12H270T00_NETGEAR&fw_sku=SKU_WW&wla_radius_ipaddr=0.0.0.0&wlg_radius_ipaddr=0.0.0.0&" \
              "wla_ent_secu_type=WPA-AUTO&wlg_ent_secu_type=WPA-AUTO&wan_ipaddr=192.168.8.8&wan_netmask=255.255.255.0&" \
              "select_2g_tpc=1&select_5g_tpc=1&wifi_2g_enable=Enable&wifi_5g_enable=Enable"%(channel,bgn_mode,width,sec,pwd)

    headers ["Referer"]="http://www.routerlogin.net/WLG_wireless_dual_band_r10.htm"
    set_req = requests.post(url=set_url,headers=headers,params=querystring,data=payload)
    #print(set_req.text)

if __name__ == "__main__":
    ssid = "NETGEAR39"
    pwd = "aylatest"
    width = 1
    channel = 2
    ap_mode = "300Mbps,WPA2-PSK"
    web_path = "C:\\Users\Sakura\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    SetRouterNETGEAR(web_path,ssid,pwd,width,channel,ap_mode)