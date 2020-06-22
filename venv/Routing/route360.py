import requests
import json
import time

from Routing.aes_key import encrypt
headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Referer':"http://ihome.360.cn/login_pc.htm"
    }
para = {

}
set_string = "wire_enable=1&AP_SSID=%s&channel_band=%d&channel_width=%d&channel_num=" \
          "%d&wire_mac=1C-68-7E-B7-CF-67&network_mode=0&radio_criterion=10&SSID_broadcast=1&" \
          "ap_id=0&port_id=WIFI1&region=3&need_reboot=0&waln_partition=0"
#response = requests.request("GET", rand_url, headers=headers, params=querystring)
def GetRand_key(url,time,password):
    querystring = {"noneed": "noneed", "_": "%d"%(time)}
    response = requests.get(url=url,params=querystring)
    #print(response.text)
    string = response.text.split("\"")[-2]
    rand_index = string[:32]
    rand_text = string[32:]
    result = str(encrypt(rand_text, "aylatest")).split('\'')[-2]
    login_pass = rand_index + result
    return login_pass
#if __name__=='__main__':
def SetRoute(web_path,ssid,password,width,channel,ap_mode):
    ssid = ssid
    password = password
    rand_url = "http://ihome.360.cn/router/get_rand_key.cgi"
    login_url = "http://ihome.360.cn/router/web_login.cgi"
    sec_url = "http://ihome.360.cn/router/wireless_sec_set.cgi"
    bas_url = "http://ihome.360.cn/router/wire_bas_ap_set.cgi"
    #band = 0
    width = width
    channel = channel
    ap_mode = ap_mode
    login_pass = GetRand_key(rand_url,int(time.time()*1000),password)          #获取随机密钥，加密

    #print(login_pass)
    payload = "user=admin&pass="+login_pass
    #print(payload)
    req = requests.post(url=login_url,headers=headers,data=payload)                     #登录路由后台
    #print(req.text)

    set_cookies = str(req.cookies).split('Cookie ')[-1].split(' ')[0]                   #获取设置Cookie
    token_id = req.text.split('\"')[-2]                                                 #获取token_id

    base_string = "wire_enable=1&AP_SSID=%s&channel_band=0&channel_width=%d&channel_num=" \
                      "%d&wire_mac=1C-68-7E-B7-CF-67&network_mode=0&radio_criterion=10&SSID_broadcast=1&" \
                      "ap_id=0&port_id=WIFI1&region=3&need_reboot=0&waln_partition=0"%(ssid,width,channel)
    sec0_string = "ap_id=0&port_id=WIFI1&ap_mode=0"

    # 拼接请求头部
    headers["token_id"] = token_id
    headers["Referer"] = "http://ihome.360.cn/new_index.htm?token_id=" + token_id
    headers["Cookie"] = set_cookies
    if ap_mode == 0:
        sec_string = "ap_id=0&port_id=WIFI1&ap_mode=0"
    else:
        web_pass = GetRand_key(rand_url, int(time.time() * 1000),password)  # 获取随机密钥，加密
        sec_string = "ap_id=0&port_id=WIFI1&ap_mode=%d&wpa_key=%s&" \
                                  "wpa_keytime=3600&wpa_mode=0&wpa_tkaes_flag=0"%(ap_mode,web_pass)

    sec_req = requests.post(url=sec_url,headers=headers,data=sec_string)    #设置配置参数
    base_req = requests.post(url=bas_url,headers=headers,data=base_string)
    if sec_req.text == "SUCCESS"and base_req.text=="SUCCESS":
        return True
    else:
        return False
if __name__=="__main__":
    ssid = "360WiFi-B7CF67"
    password = "aylatest"
    width = 3
    channel = 12
    ap_mode = 0
    web_path = "C:\\Users\Sakura\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    try:
        SetRoute(web_path,ssid,password,width,channel,ap_mode)
        print("set success!")
    except Exception as e:
        print("设置路由失败")