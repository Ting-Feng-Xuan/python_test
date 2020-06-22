
import xlrd
import xlwt         #最大支持65536行数据
from xlutils.copy import copy

def write_new_excel():
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet(u"sheet1")
    worksheet.write(5,5,1234)
    workbook.save("./demo1.xlsx")
    return worksheet
def write_excel_by_row(file_path,worksheet,row,data):
    try:
        oldwd = xlrd.open_workbook(file_path,formatting_info=True)
        newwd = copy(oldwd)
        try:
            newws = newwd.get_sheet(worksheet)
        except IndexError:
            newws = newwd.add_sheet(u"sheet%d"%(worksheet+1))
    except FileNotFoundError:
        newwd = xlwt.Workbook()
        newws = newwd.add_sheet(u"sheet%d"%(worksheet+1))
    i = 0
    for key in data:
        newws.write(row,i,data[key])
        i +=1
    newwd.save(file_path)
def write_excel_by_column(file_path,worksheet,column,data):
    try:
        oldwd = xlrd.open_workbook(file_path, formatting_info=True)
        newwd = copy(oldwd)
        newws = newwd.get_sheet(worksheet)
    except IndexError:
        newws = newwd.add_sheet(u"sheet%d"%(worksheet+1))
    except FileNotFoundError:
        newwd = xlwt.Workbook()
        newws = newwd.add_sheet(u"sheet%d" % (worksheet+1))
    i = 0
    for key in data:
        newws.write(i,column,data[key])
        i +=1
    newwd.save(file_path)
def get_excel_rows(file_path,worksheet):
    try:
        workbook = xlrd.open_workbook(file_path)
        table = workbook.sheets()[worksheet]
        return int(table.nrows)
    except FileNotFoundError:
        return 0
    except IndexError:
        return 0
if __name__ =="__main__":
    data = {"1":0,"2":3,"4":7}

    write_excel_by_row("C:/Users/Sakura/Desktop/Python_test/venv/Routing/result/result-2019-12-19-17-16-43.xls",0,get_excel_rows("C:/Users/Sakura/Desktop/Python_test/venv/Routing/result/result-2019-12-19-17-16-43.xls",  0),data)
    #get_excel_rows("C:/Users/Sakura/Desktop/Python_test/venv/Routing/result-2019-12-17-17:53:35.xls",0)