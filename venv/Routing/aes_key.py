
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


# 如果text不足16位的倍数就用空格补足为16位
def bytePad(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + (chr(8) * add) #这里写死填充8
    return text.encode('utf-8')

# 加密函数
def encrypt(rand_key,text):
    key = a2b_hex(rand_key) # randkey后32位
    #print(key)
    mode = AES.MODE_CBC
    iv = b'360luyou@install' # 360 aes加密 cbc模式下的iv向量
    #print(iv)
    text = bytePad(text)
    #print(text)
    cryptos = AES.new(key, mode, iv)
    cipher_text = cryptos.encrypt(text)
    # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
    return b2a_hex(cipher_text)

if __name__ == '__main__':
    e = encrypt("","aylatest")
    print("加密:", e)