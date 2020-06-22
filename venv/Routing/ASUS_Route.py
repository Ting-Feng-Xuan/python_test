import requests
import os

def SetASUS_Router(web_path,ssid,pwd,width,channel,ap_mode):

    url = "http://router.asus.com/login.cgi"
    payload = "group_id=&action_mode=&action_script=&action_wait=5&current_page=Main_Login.asp&next_page=index.asp&login_authorization=YWRtaW46YXlsYXRlc3Q%3D"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded;",
        'Referer': "http://router.asus.com/Main_Login.asp",
    }
    response = requests.post(url, headers=headers, data=payload)
    cookies = str(response.cookies).split(' ')[-3]

    sec = ap_mode.split('-')[0]                  #加密方式
    bgn_mode = ap_mode.split('-'[-1])
    url = "http://router.asus.com/start_apply2.htm"

    payload = "productid=RT-AC1200&current_page=Advanced_Wireless_Content.asp&next_page=Advanced_Wireless_Content.asp&" \
              "modified=0&action_mode=apply_new&action_script=restart_wireless&action_wait=5&preferred_lang=CN&firmver=3.0.0.4&" \
              "wps_mode=&wps_config_state=1&wl_wpa_psk_org=aylatest&wl_key1_org=&wl_key2_org=&wl_key3_org=&wl_key4_org=&" \
              "wl_phrase_x_org=&x_RegulatoryDomain=&wl_gmode_protection=%s&wl_wme=auto&wl_mode_x=0&wl_nmode=&wl_nctrlsb_old=upper&" \
              "wl_key_type=&wl_channel_orig=&AUTO_CHANNEL=&wl_wep_x_orig=0&wl_optimizexbox=&wl_subunit=-1&wps_enable=1&w_Setting=1&" \
              "wl_unit=0&wl_ssid=ASUS&wl_closed=0&wl_nmode_x=0&wl_gmode_check=&wl_bw=%d&wl_channel=%d&wl_nctrlsb=upper&" \
              "wl_auth_mode_x=%s&wl_crypto=aes&wl_wpa_psk=aylatest&wl_wpa_gtk_rekey=3600"%(bgn_mode,width,channel,sec)

    headers['Cookie'] = cookies
    headers['Referer'] = 'http://router.asus.com/Advanced_Wireless_Content.asp'
    response = requests.request("POST", url, data=payload, headers=headers)

    #print(headers)


if __name__=="__main__":
    ssid = "ASUS"
    pwd = "aylatest"
    width = 0
    channel = 9
    ap_mode = ('psk2-auto','open-auto','psk-auto','pskpsk2-auto','psk2-off')
    web_path = "C:\\Users\Sakura\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    for i in range(5):
        SetASUS_Router(web_path,ssid,pwd,width,channel,ap_mode[i])