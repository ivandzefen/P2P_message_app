import socket
import constants
import subprocess
import mysql.connector
try:
    from getmac import get_mac_address
    def gma() :
        return get_mac_address()
except ModuleNotFoundError :
    import uuid
    def gma():
        return ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
def get_ip() :
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(('8.8.8.8',80))
    ip=s.getsockname()[0]
    s.close()
    return ip

tr

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

def db_to_str(dbval) :
    ans=dbval
    for i in range(len(ans)) :
        ans[i]=list(ans[i][:-1])
        for j in range(len(ans[i])):
            ans[i][j]=str(ans[i][j])
        ans[i]='°'.join(ans[i])
    ans='|'.join(ans)
    return ans

def get_user_list(conn=None,name=None):
    if not conn:
        conn=utilities.send_msg(constants.GET_USER_LIST,constants.SERVER_IP,name,gma(),constants.SERVER_MAC)
    msg=recieve_msg(conn)
    disconnect=constants.DISCONNECT_MESSAGE.encode(constants.FORMAT)
    lengthd=str(len(disconnect)).encode(constants.FORMAT)
    lengthd+=b' '*(constants.HEADER-len(lengthd))
    conn.send(lengthd)
    conn.send(disconnect)
    conn.close()
    if msg[2]==constants.SERVER_MAC:
        user_list=dbstr_to_lst(msg[0])
    return user_list

def dbstr_to_lst(dbstr) :
    lst=dbstr.split('|')
    ans={}
    for i in range(len(lst)):
        lst[i]=lst[i].split('°')
        ans[lst[i][0]]=lst[i][1:].append(0)
    return ans

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
    if msg==constants.GET_USER_LIST :
        return conn
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

def connect_to_db(db_config) :
    connected=False
    while not connected :
        try :
            conn=mysql.connector.connect(**db_config)
            connected=True
            print('connected to database')
            return conn
        except Exception as e :
                print(e)
                return
