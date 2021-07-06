from Cryptodome.Cipher import AES
from curve import *
import secrets
import hashlib

curve = secp256k1
def compress_point(point):
    return hex(point.x)+hex(point.y % 2)[2:]

short = lambda x: len(x)>32 and x[:32] or x

#key genaration for tramission
def transkeygen(pubkey):
    key = "{0}:{1}".format(pubkey.x,pubkey.y)
    return key
    
#key generation for encryption
def concadekey(curve,key):
        k = key
        pad = ':'
        pad_index = k.find(pad)
        x = k[:pad_index]
        y = k[pad_index + 1 :]
        compub = ECpoint(curve,int(x),int(y))
        return compub
        

#input_plaintext
def inplaintext(info):
    msg = info
    length = len(msg)
    h = hashlib.md5(msg.encode('utf-8')).hexdigest()
    in_msg = msg + h + str(length)
    return in_msg

#output plaintext
def outplaintext(info):
    msg = info
    l = len(msg)
    strs = msg[-1]
    size = int(strs)
    message = msg[:size]
    #h = msg[size:l-1]
    #ver =  hashlib.md5(message.encode('utf-8')).hexdigest()

    return message


#Encryption
def encrypt(msg, key):
    msg = inplaintext(msg)
    Block_size = 128
    pad = "{"
    padding = lambda s: s + (Block_size - len(s) % Block_size) * pad
    cipher = AES.new(short(key.encode('utf-8')), AES.MODE_ECB)
    result = cipher.encrypt(padding(msg).encode('utf-8'))
    return result


#Decryption
def decrypt(msg, key):
    pad = b"{"
    decipher = AES.new(short(key.encode('utf-8')), AES.MODE_ECB)
    #msg = bytes(msg,'utf-8')
    #print(msg,'\n',type(msg))
    pt = decipher.decrypt(msg)#.decode('utf-8')
    pad_index = pt.find(pad)
    result = pt[:pad_index]
    #return outplaintext(result)
    return result

