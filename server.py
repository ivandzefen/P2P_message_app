import socket
import threading
import utilities
import constants
import time


IP=utilities.get_ip()
ADDR=(IP,constants.PORT)
username=''

def handleclient(conn,addr,user_list,username):
    connected=True
    ip=addr[0]
    while connected:
        msg=utilities.recieve_msg(conn)
        if not msg:
            continue
        ymac=msg[2]
        if msg[0]==constants.PING_MSG:
            utilities.sendmsg(username,conn)
        elif msg[0]==constants.DISCONNECT_MESSAGE:
            connected=False
        else :
            if ymac not in user_list:
                user_list[ymac]=[ip,msg[1],0,[]]
            print(f'[NEW MESSAGE] {user_list[ymac][1]} : {msg[0]}\n->',end='')
            if not user_list[ymac][2] :
                user_list[ymac][3].append(msg[0])
    conn.close()

def recieving(server,user_list,username) :
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handleclient,args=(conn,addr,user_list,username))
        thread.start()

def start(user_list,checkvalues):
    //username=str(input('please enter a username : '))
    //checkvalues['username']=username
    utilities.ping(utilities.gma(),utilities.get_ip(),username)
    utilities.get_user_list(lst=user_list)
    checkvalues['updating']=False
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    thread=threading.Thread(target=recieving,args=(server,user_list,username))
    thread.start()
    while True:
        utilities.ping(utilities.gma(),utilities.get_ip(),username)
        time.sleep(3)
        #print(f'[CONNECTED] {threading.active_count()-1}')
        if checkvalues['update_table'] :
            user_list={}
            checkvalues['update_table']=False
            utilities.get_user_list(lst=user_list)
            checkvalues['updating']=False

if __name__=='__main__':
    start(user_list={},checkvalues={'updating':True,'update_table':True})
