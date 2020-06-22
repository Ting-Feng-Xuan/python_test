import time
import os
import requests

def SetRouteDLink(web_path,ssid,password,width,channel,ap_mode):
    url = "http://192.168.0.1/goform/setWifi"
    sec = ap_mode.split("-")[0]

    bgn_mode = ap_mode.split('-')[1]
     #WPAWPA2%2FAES
    payload = "module1=wifiBasicCfg&doubleBandUnityEnable=false&wifiTotalEn=true&wifiEn=true&wifiSSID=D-Link_DIR-823G&" \
              "wifiSecurityMode=%s&wifiPwd=aylatest&wifiHideSSID=false&wifiEn_5G=true&wifiSSID_5G=D-Link_DIR-823G_5G&" \
              "wifiSecurityMode_5G=NONE&wifiPwd_5G=&wifiHideSSID_5G=false&module2=wifiGuest&guestEn=false&guestEn_5G=false&" \
              "guestSSID=D-Link_Guest&guestSSID_5G=D-Link_Guest_5G&guestPwd=&guestPwd_5G=&guestValidTime=8&guestShareSpeed=0&" \
              "module3=wifiPower&wifiPower=high&wifiPower_5G=high&module5=wifiAdvCfg&wifiMode=%s&wifiChannel=%d&wifiBandwidth=%s&" \
              "wifiMode_5G=ac&wifiChannel_5G=auto&wifiBandwidth_5G=auto&wifiAntijamEn=false&module6=wifiBeamforming&" \
              "wifiBeaformingEn=true&module7=wifiWPS&wpsEn=true"%(sec,bgn_mode,channel,width)

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Referer': "http://192.168.0.1/index.html",
        'Cookie': "ecos_pw=1qw:language=cn",
        'User-Agent': "PostmanRuntime/7.20.1",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "120c31d4-a7b4-498d-8a34-aed94068b18f,ac90b980-d241-42d8-a353-df1805275f1f",
        'Host': "192.168.0.1",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "697",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }
    result = requests.post(url=url,headers=headers,data=payload)
    print(result.text)

if __name__ =="__main__":
    ssid = "D-Link_DIR-823G"
    password = "aylatest"
    width = "20"
    channel = 6
    ap_mode = "WPA/AES-bg-20"
    web_path = "C:\\Users\Sakura\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    SetRouteDLink(web_path,ssid,password,width,channel,ap_mode)