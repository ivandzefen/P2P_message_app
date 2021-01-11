import socket
import constants
import subprocess
import uuid
from getmac import get_mac_address

try :
    import requests
except ModuleNotFoundError :
    import pip
    pip.main(['install','requests'])
    import requests

def gma() :
    mac1=get_mac_address()
    mac2=':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
    return mac1 if mac1 else mac2

def _url(endpoint) :
    return constants.SERVER_URL+endpoint

def get_ip() :
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(('8.8.8.8',80))
    ip=s.getsockname()[0]
    s.close()
    return ip
def ping(mac,ip,username):
    res=requests.post(_url('/ping'),json={'mac':mac,'ip':ip,'username':username})
def recieve_msg(conn,mmac=gma()) :
    msg_head=conn.recv(constants.HEADER).decode(constants.FORMAT)
    if msg_head:
        msg_length=int(msg_head.split(' ')[0])
        user_name=msg_head.split(' ')[1]
        mac=msg_head.split(' ')[2]
        revr=msg_head.split(' ')[3]
        msg=conn.recv(msg_length)
        msg=msg.decode(constants.FORMAT)
        if revr==mmac :
            return (msg,user_name,mac)
        else :
            return ''
    else :
        return ''

def db_to_json(dbval) :
    ans=[]
    #for i in range(len(ans)) :
    #    ans[i]=list(ans[i][:-1])
    #    for j in range(len(ans[i])):
    #        ans[i][j]=str(ans[i][j])
    #    ans[i]='°'.join(ans[i])
    #ans='|'.join(ans)
    for i in dbval :
        a={'mac':i[0],'ip':i[1],'username':i[2]}
        ans.append(a)
    return ans

def get_user_list(lst,conn=None,name=None):
    #if not conn:
    #    conn=send_msg(constants.GET_USER_LIST,constants.SERVER_IP,name,gma(),constants.SERVER_MAC)
    #msg=recieve_msg(conn)
    #disconnect=constants.DISCONNECT_MESSAGE.encode(constants.FORMAT)
    #lengthd=str(len(disconnect)).encode(constants.FORMAT)
    #lengthd+=b' '*(constants.HEADER-len(lengthd))
    #conn.send(lengthd)
    #conn.send(disconnect)
    #conn.close()
    #if msg[2]==constants.SERVER_MAC:
    res=requests.get(_url('/online_users'))
    json=res.json()
    json_to_lst(json,lst)


def json_to_lst(json,last) :
    for i in json:
        lst=[i['ip'],i['username']]
        lst.append(0)
        lst.append([])
        last[i['mac']]=lst

def send_msg(msg,ip,username,my_mac,your_mac):
    conn=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try :
        conn.connect((ip,constants.PORT))
    except :
        print("user might be offline")
        return None
    message=msg.encode(constants.FORMAT)
    length=str(len(message)).encode(constants.FORMAT)
    length+=b' '
    length+=username.encode(constants.FORMAT)
    length+=b' '
    length+=my_mac.encode(constants.FORMAT)
    length+=b' '
    length+=your_mac.encode(constants.FORMAT)
    length+=b' '*(constants.HEADER-len(length))
    disconnect=constants.DISCONNECT_MESSAGE.encode(constants.FORMAT)
    lengthd=str(len(disconnect)).encode(constants.FORMAT)
    lengthd+=b' '*(constants.HEADER-len(lengthd))
    conn.send(length)
    conn.send(message)
    conn.send(lengthd)
    conn.send(disconnect)
    conn.close()
    return None

def sendmsg(msg,conn,username,my_mac,your_mac):
    message=msg.encode(constants.FORMAT)
    length=str(len(message)).encode(constants.FORMAT)
    length+=b' '
    length+=username.encode(constants.FORMAT)
    length+=b' '
    length+=my_mac.encode(constants.FORMAT)
    length+=b' '
    length+=your_mac.encode(constants.FORMAT)
    length+=b' '*(constants.HEADER-len(length))
    disconnect=constants.DISCONNECT_MESSAGE.encode(constants.FORMAT)
    lengthd=str(len(disconnect)).encode(constants.FORMAT)
    lengthd+=b' '*(constants.HEADER-len(lengthd))
    conn.send(length)
    conn.send(message)
    return None
