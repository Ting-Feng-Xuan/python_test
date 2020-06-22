import requests


def SetTenda_Route(web_path, ssid, pwd, width, channel, ap_mode):

    bgn_mode = ap_mode.split('-')[-2]
    set_width = ap_mode.split('-')[-1]
    sec = ap_mode.split('-')[0]
    url = "http://192.168.0.1/goform/setWifi"
    payload = 'module1=wifiBasicCfg&wifiEn=true&wifiSSID=Tenda68&wifiSecurityMode={}&' \
              'wifiPwd={}&' \
              'wifiHideSSID=false&module5=wifiAdvCfg&wifiMode={}&' \
              'wifiChannel={}&' \
              'wifiBandwidth={}&' \
              'wifiAntijamEn={}&'\
              'module4=wifiTime&wifiTimeEn=false&wifiTimeClose=00%3A00-07%3A00&wifiTimeDate=01111100'.format(sec,pwd,bgn_mode,channel,set_width,width)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://192.168.0.1/index.html',
        'Cookie': 'ecos_pw=1qw:language=cn'
    }
    ser_req = requests.post(url=url,headers=headers,data= payload)


if __name__ == "__main__":
    ssid = "Tenda68"
    pwd = "aylatest"
    width = "false"
    channel = 9
    ap_mode = "WPAWPA2/AES-bgn-auto"
    web_path = "C:\\Users\Sakura\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    SetTenda_Route(web_path, ssid, pwd, width, channel, ap_mode)