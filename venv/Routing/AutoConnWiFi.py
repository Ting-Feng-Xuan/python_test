import urllib
import urllib3
import os
import time
import re
import subprocess

import xml.dom.minidom
import xml.etree.cElementTree as ET
from binascii import b2a_hex, a2b_hex

def read_xml(path):
    tree = ElementTree()
    tree.parse(path)
    return tree
def write_xml(tree,out_path):
    tree.write(out_path,encoding="utf-8",xml_declaration = True)

def if_match(node,kv_map):
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True
def find_node(tree,path):
    return tree.findall(path)
def change_node_properties(nodelist,kv_map,isdelete = False):
    for node in nodelist:
        for key in kv_map:
            if isdelete:
                if key in node.attrib:
                    del node.attrib[key]
                else:
                    node.set(key,kv_map.get(key))
def Is_Exist(parent,node_name):

  try:
      str(parent[1].tag)
      return True
  except Exception as e:
      return False

def connect_wifi(ssid,keyMaterial,sec):

    #创建 wifi配置xml文件
    ET.register_namespace('', "http://www.microsoft.com/networking/WLAN/profile/v1")    #放在parse之前
    ET.register_namespace('xsi', "http://www.microsoft.com/networking/WLAN/profile/v3")
    tree =  ET.parse("C:\\Users\Sakura\Desktop\Python_test\\venv\Routing\wifi_conf.xml")
    ns1 = {"http://www.microsoft.com/networking/WLAN/profile/v1"}
    ns2 = {"http://www.microsoft.com/networking/WLAN/profile/v3"}
    root = tree.getroot()

    #for child in root:
     #   print(child.tag)
    #print("\n")

    ssid_conf = b2a_hex(ssid.encode('utf-8'))
    ssid_conf = str(ssid_conf).split('\'')[-2]
    root[0].text = ssid
    root[1][0][1].text = ssid
    root[1][0][0].text = ssid_conf
    node_parent = root[4][0]

    if sec == "":
        root[4][0][0][0].text = "open"
        root[4][0][0][1].text = "none"
        if Is_Exist(node_parent, "sharedKey"):
            node_parent.remove(root[4][0][1])
    else:
        root[4][0][0][0].text = "WPA2PSK"
        root[4][0][0][1].text = "AES"
        if Is_Exist(node_parent,"sharedKey")==False:
            element = ET.Element("sharedKey")
            node_parent.append(element)

            one = ET.Element("keyType")
            one.text = "passPhrase"
            element.append(one)

            two = ET.Element("protected")
            two.text = "true"
            element.append(two)

            three = ET.Element("keyMaterial")
            three.text = keyMaterial
            element.append(three)
        #print(root[4][0][1].tag)
    tree.write("C:\\Users\Sakura\Desktop\Python_test\\venv\Routing\wifi_conf.xml")
    time.sleep(2)
    cmd_result = subprocess.Popen("netsh wlan add profile filename=C:/Users/Sakura/Desktop/Python_test/venv/Routing/wifi_conf.xml", stdout=subprocess.PIPE)
    result = cmd_result.stdout.read().decode("gbk")
    time.sleep(1)
    cmd_result = subprocess.Popen("netsh wlan connect name=%s"%(ssid), stdout=subprocess.PIPE)
    result = cmd_result.stdout.read().decode("gbk")
    time.sleep(10)
    if Is_connected(ssid) == True:
        return True
    print("wifi连接失败,请尝试手动重连!")
    return False

def Is_connected(ssid):
   cmd_result = subprocess.Popen("netsh wlan show interface",stdout=subprocess.PIPE)
   result = cmd_result.stdout.read().decode("gbk")
   #print(result)
   #print(result.find('已连接'))
   #print(result.find(ssid))
   if result.find('已连接')!=-1 and result.find(ssid)!= -1:
       print("ssid :%s 状态:连接成功"%(ssid))
       return True
   return False

if __name__=="__main__":
    ssid = "TP-LINK_D841"
    pwd = ""
    sec = "11"
    keyMaterial = "01000000D08C9DDF0115D1118C7A00C04FC297EB01000000347E492CCEF92F4B8C3D953EDD719F8000000000020000000000106600000001000020000000743E34B63E23EBF732947DFDEADDB2D8DA3EBA04057F7B89B7269FECFD28EA25000000000E80000000020000200000002F1E05CC303935F6A4379664E848123BB103A60BD5D908A4F2178026A42F5E491000000074700635BEEC7DAE9907CCDD07D95ECC40000000FDB788B0AE03D3B24D07A8A0C340FF830941987CF2F478AC686B33747EE593C8B7D90981C3C26C051E11F67E6BA9B1E0044A9D756197D7648A38503FB78A2532"
    connect_wifi(ssid,keyMaterial,sec)
    #Is_connected(ssid)
