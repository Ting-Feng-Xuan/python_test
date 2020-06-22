from xlutils.copy import copy
import xlrd

# 将数据写入excel文件,path:excel文件路径,row:行数,data:写入的数据
def write_excel(path,row,data,time,data1,time1,all_time,data2,time2,data3,time3,all_time1):
    rb = xlrd.open_workbook(path)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    ws.write(row,1,data)
    ws.write(row,2,time)
    ws.write(row,3,data1)
    ws.write(row,4,time1)
    ws.write(row,5,all_time)


    ws.write(row,7,data2)
    ws.write(row,8,time2)
    ws.write(row,9,data3)
    ws.write(row,10,time3)
    ws.write(row,11,all_time1)

    wb.save(path)