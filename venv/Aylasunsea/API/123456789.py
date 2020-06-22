import requests
import time
import datetime
from Aylasunsea.Public_Module.Time_Now import get_time_stamp
from datetime import datetime

if __name__ == '__main__':
    now_time = get_time_stamp()
    print(now_time)
    print(now_time[0])
    print(now_time[1])
    all_time = round((result1[2] - now_time[1]), 3)