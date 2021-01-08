import socket
import utilities
import constants
import server
import threading
import time
import datetime

def begin():
    user_list=[]
    mac=utilities.gma()
    checkvalues={'update_table':False,'updating':True,'username':''}
    done=False
    print(user_list)
    s_thread=threading.Thread(target=server.start,args=(user_list,checkvalues))
    s_thread.start()
    while True :

        while checkvalues['updating']:
            #print('waiting')
            time.sleep(3)
        list=[]
        #print('here')
        username=checkvalues['username']
        for i in user_list :
            list.append(i)
        if  not len(list) :
            ans=input('no connected users. Wait ?(y/n)')
            if 'y' in ans.lower() :
                while not len(list) :
                    utilities.get_connected_users(user_list)
                    for i in user_list :
                        list.append(i)
                    print('waiting...')
                    time.sleep(3)
            else :
                checkvalues['update_table']=True
                checkvalues['updating']=True
        if not len(list):
            continue
        print('ONLINE')
        for i in range(len(list)):
            print(f'{i+1} : {user_list[list[i]][1]}')
        chat=0
        while not chat :
            try :
                chat=int(input('select a user whit whom you want to chat'))
                if (chat-1) not in range(len(list)) :
                    print('select a valid user')
                    chat=0
            except :
                print('select a valid user')
        chat=chat-1
        inchat=True and len(list)
        ymar=list[chat]
        name=user_list[ymac][1]
        ip=user_list[ymac][0]
        user_list[ymac][2]=1
        print(f'chatting with {name} enter EXIT to quit this chat')
        while inchat :
            for i in range(len(user_list[ip][1])):
                print(f'{name} : {user_list[ip][1].pop(0)}')
            msg=str(input('->'))
            if msg=='EXIT' :
                inchat=False
                user_list[ip][2]=0
                checkvalues['update_table']=True
                checkvalues['updating']=True
                continue
            utilities.send_msg(msg,ip,username,mac)

if __name__=='__main__' :
    begin()
