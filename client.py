import socket
import utilities
import constants
from getmac import get_mac_address as gma

IP=utilities.get_ip()
ADDR=(IP,constants.PORT)


def chat(addr):
    ip=constants.SERVER_IP
    name='server'
    inchat=True
    username='black'
    mac=gma()
    print(f'chatting with {name} enter EXIT to quit this chat')
    while inchat :
        #for i in range(len(user_list[ip][1])):
        #    print(f'{name} : {user_list[ip][1].pop(0)}')
        msg=str(input('->'))
        if msg=='EXIT' :
            inchat=False
            #user_list[ip][2]=0
            #checkvalues['update_table']=True
            #checkvalues['updating']=True
            continue
        conn=utilities.send_msg(msg,ip,username,mac,constants.SERVER_MAC)
        if msg==constants.GET_USER_LIST :
            print(conn)
            user_list=utilities.get_user_list(conn=conn)
            for i in user_list:
                print(i)

if __name__=='__main__':
    chat(ADDR)
