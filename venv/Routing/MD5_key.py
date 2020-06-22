import hashlib




def GetMD5Key(data):
    data_len = len(data)
    if len(data) < 10:
        data += "0"
        data += str(data_len)
        print(data_len)
    else:
        data += str(data_len)
    data_len += 2
    print(data)
    key_str = data
    while len(key_str) < 64:
        key_str += data
    if len(key_str) != 64:
        key_str = key_str[:64]
    print(key_str)
    md5_obj = hashlib.md5()
    md5_obj.update(key_str.encode('utf-8'))
    reaslut = md5_obj.hexdigest()
    #reaslut = hashlib.md5(key_str.encode())
    #reaslut = hashlib
    return reaslut

if __name__=="__main__":
    pwd = "aylatest"
    GetMD5Key(pwd)