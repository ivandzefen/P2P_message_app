import socket
import threading
import utilities
import constants
from getmac import get_mac_address as gma

IP=utilities.get_ip()
ADDR=(IP,constants.PORT)
username=''

def handleclient(conn,addr,user_list,username):
    connected=True
    ip=addr[0]
    while connected:
        msg=utilities.recieve_msg(conn)
        if not msg:
            pass
        elif msg[0]==constants.PING_MSG:
            utilities.sendmsg(username,conn)
        elif msg[0]==constants.DISCONNECT_MESSAGE:
            connected=False
        else :
            if ip not in user_list:
                user_list[ip]=[msg[1],[],0]
            print(f'[NEW MESSAGE] {user_list[ip][0]} : {msg[0]}')
            if not user_list[ip][2] :
                user_list[ip][1].append(msg[0])
    conn.close()
def showLife():
    while True:
        utilities.send_msg(constants.PING_MSG,constants.SERVER_IP,checkvalues['username'],utilities.gma(),constants.SERVER_MAC)
        sleep(10)

def start(user_list,checkvalues):
    showLife()
    username=str(input('please enter a username : '))
    checkvalues['username']=username
    user_list=utilities.get_connected_users(name=username)
    checkvalues['updating']=False
    print('hey')
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)
    print(f'[STARTING] Server starting')
    server.listen()
    print(f'[LISTENING] listening at {ADDR}')
    while True:
        #print('listening')
        conn,addr = server.accept()
        thread = threading.Thread(target=handleclient,args=(conn,addr,user_list,username))
        thread.start()
        #print(f'[CONNECTED] {threading.active_count()-1}')
        if checkvalues['update_table'] :
            user_list={}
            checkvalues['update_table']=False
            utilities.get_connected_users(user_list)
            checkvalues['updating']=False

if __name__=='__main__':
    start(user_list={},checkvalues={'updating':True,'update_table':True})
