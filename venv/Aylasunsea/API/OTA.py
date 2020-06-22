import requests
import time
import json


# 通过设备组ID、镜像ID创建OTA工作
def CreatOTAjob(headers,Server,OTAData):
    if Server == '-dev.ayla.com.cn':
        server = '.ayla.com.cn'
    else:
        server = Server
    ads_url1 = "https://ais%s/imageservice/v1/job.json?env=ssct" %server
    data = json.dumps(OTAData)
    try:
        res_control = requests.post(url=ads_url1, headers=headers, data=data).json()
    except Exception as e:
        print('CreatOTAjob控制请求超时')
        time.sleep(1)
        # CreatOTAjob()
        return 'CreatOTAjob NO'
    print(res_control)
    if "job" in res_control:
        jobID = res_control["job"]["id"]
    elif "id" in res_control:
        jobID = res_control["id"]

    return jobID

# 通过OTA工作的ID，执行开始
def StartOTAjob(headers,Server,jobID):
    if Server == '-dev.ayla.com.cn':
        server = '.ayla.com.cn'
    ads_url1 = "https://ais%s/imageservice/v1/job/%s/start.json?env=ssct" %(server,jobID)
    data = json.dumps({})
    try:
        res_control = requests.post(url=ads_url1, headers=headers, data=data).json()
    except Exception as e:
        print('StartOTAjob控制请求超时')
        time.sleep(1)
        StartOTAjob()
    return 'StartOTAjob OK'

# 通过OTA工作的ID，获取执行的状态
def GetOTAstatus(headers,Server,jobID):
    if Server == '-dev.ayla.com.cn':
        server = '.ayla.com.cn'
    ads_url1 = "https://ais%s/imageservice/v1/job/%s.json?env=ssct&base=true" %(server,jobID)
    data = json.dumps({})
    try:
        res_control = requests.get(url=ads_url1, headers=headers, data=data).json()
    except Exception as e:
        print('GetOTAstatus控制请求超时')
        time.sleep(1)
        GetOTAstatus()
    status = res_control['succeed_count']

    return status





# {"group_id": "513", "image_id": 1000499, "name": "bk_2-1", "sw_version": "1.0"}
# {"group_id":"513","image_id":1000500,"name":"bk_1-2","sw_version":"2.0"}


# {"group_id":"513","image_id":1000510,"name":"w600_2-1","sw_version":"1.0"}
# {"group_id":"513","image_id":1000511,"name":"w600_1-2","sw_version":"2.0"}



# {"id":1000609,"name":"bk_6-7","status":"initialized","creation_date":"2019-07-11T10:03:48Z","last_updated_at":"2019-07-11T10:03:48Z","device_count":1,"failed_count":0,"succeed_count":0,"in_progress_count":0,"user_id":13807}