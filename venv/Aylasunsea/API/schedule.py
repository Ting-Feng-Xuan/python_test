import requests
import time
import json


# 设置定时器
def Schedule(headers,server,Device_id,sch_id,T):

    ct = time.time()
    print(ct)
    CT = ct +T        #设置定时器在T秒后执行
    print(CT)
    Localtime = time.localtime(CT)
    print(Localtime)
    start_time_each_day = time.strftime("%H:%M:%S",Localtime)
    print(start_time_each_day)
    name = 'sch0'
    start_date = time.strftime("%Y-%m-%d",Localtime)
    print(start_date)
    # start_date = "2019-07-02"
    # start_time_each_day = "13:45:00"
    sch_key = sch_id
    action_key = 119391
    ads_url = "https://ads-%s/apiv1/devices/%s/schedules/%s.json?env=ssct" %(server,Device_id,sch_id)
    data = json.dumps({"id":sch_key,"device_id":Device_id,"schedule":{"active":True,"day_occur_of_month":[],"days_of_month":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],"days_of_week":[1,2,3,4,5,6,7],"device_id":Device_id,"direction":"input","display_name":name,"duration":None,"end_date":"","end_time_each_day":"23:59:59","fixed_actions":False,"interval":None,"months_of_year":[1,2,3,4,5,6,7,8,9,10,11,12],"name":name,"start_date":start_date,"start_time_each_day":start_time_each_day,"time_before_end":None,"utc":False,"version":"1","key":sch_key,"schedule_actions":[{"name":"Percent_Control","base_type":"integer","in_range":False,"at_start":True,"at_end":False,"active":True,"key":action_key,"value":66}]}})
    try:
        res_control = requests.put(url=ads_url, headers=headers, data=data).json()
    except Exception as e:
        print('Schedule请求超时')
        # time.sleep(1)
        # LanON()
        return 'Schedule NO'
    print(res_control)
    return 'Schedule OK'
#

# {"id":60783,"device_id":15693214,"schedule":{"active":true,"day_occur_of_month":[],"days_of_month":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],"days_of_week":null,"device_id":15693214,"direction":"input","display_name":"sch0","duration":0,"end_date":"","end_time_each_day":"23:59:59","fixed_actions":false,"interval":0,"months_of_year":[1,2,3,4,5,6,7,8,9,10,11,12],"name":"sch0","start_date":"2019-11-14","start_time_each_day":"17:00:00","time_before_end":null,"utc":false,"version":"1","key":60783,"schedule_actions":[{"name":"Percent_Control","base_type":"integer","in_range":false,"at_start":true,"at_end":false,"active":true,"key":119391,"value":100}]}}


# {"id":1092072,"device_id":9257,"schedule":{"active":true,"day_occur_of_month":[],"days_of_month":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],"days_of_week":null,"device_id":9257,"direction":"input","display_name":"sch0","duration":0,"end_date":"","end_time_each_day":"00:00:00","fixed_actions":false,"interval":0,"months_of_year":[1,2,3,4,5,6,7,8,9,10,11,12],"name":"sch0","start_date":"2019-07-13","start_time_each_day":"00:00:00","time_before_end":null,"utc":false,"version":"1","key":1092072,"schedule_actions":[{"name":"Switch_Control","base_type":"boolean","in_range":false,"at_start":true,"at_end":false,"active":true,"key":1216752,"value":0}]}}

#{"id":1091951,"device_id":8135,"schedule":{"active":true,"day_occur_of_month":[],"days_of_month":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],"days_of_week":[1,2,3,4,5,6,7],"device_id":8135,"direction":"input","display_name":"sch0","duration":0,"end_date":"","end_time_each_day":"05:05:00","fixed_actions":false,"interval":0,"months_of_year":[1,2,3,4,5,6,7,8,9,10,11,12],"name":"sch0","start_date":"2019-07-12","start_time_each_day":"05:05:00","time_before_end":null,"utc":false,"version":"1","key":1091951,"schedule_actions":[{"name":"Switch_Control","base_type":"boolean","in_range":false,"at_start":true,"at_end":false,"active":true,"key":1216527,"value":1}]}}
# {"id":1090195,"device_id":8135,"schedule":{"active":true,"day_occur_of_month":[],"days_of_month":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],"days_of_week":[1,2,3,4,5,6,7],"device_id":8135,"direction":"input","display_name":"sch0","duration":0,"end_date":"","end_time_each_day":"02:01:00","fixed_actions":false,"interval":0,"months_of_year":[1,2,3,4,5,6,7,8,9,10,11,12],"name":"sch0","start_date":"2019-07-05","start_time_each_day":"02:01:00","time_before_end":null,"utc":false,"version":"1","key":1090195,"schedule_actions":[{"name":"Switch_Control","base_type":"boolean","in_range":false,"at_start":true,"at_end":false,"active":true,"key":1214483,"value":1}]}}