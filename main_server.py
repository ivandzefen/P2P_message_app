import socket
import utilities
import constants
import time
import datetime
import threading
import mysql.connector

IP=utilities.get_ip()
ADDR=(IP,constants.PORT)
DATABASE='P2P_MESSAGE_APP'
HOST='127.0.0.1'
PASSWORD='pép-server'
USER='p2p-server'
db_config={'host':HOST,
           'user':USER,
           'password':PASSWORD,
           'database':DATABASE}

def handleclient(conn,addr):
    connected=True
    ip=addr[0]
    while connected:
        msg=utilities.recieve_msg(conn,mmac=constants.SERVER_MAC)
        if not msg:
            pass
        elif msg[0]==constants.PING_MSG:
            addUser(mac=msg[2],username=msg[1],ip=ip)
        elif msg[0]==constants.GET_USER_LIST:
            utilities.sendmsg(onlineusers(),conn,'MAIN_SERVER',constants.SERVER_MAC,msg[2])
            print(f'sent to {msg[2]},{ip}')
        else :
            print(msg)
    conn.close()

def onlineusers():
    check_DB()
    try :
        conn=utilities.connect_to_db(db_config)
        cursor=conn.cursor()
        print("cursor created")
        sql="""SELECT * FROM onlineUsers"""
        cursor.execute(sql)
        print("sql executed")
        ans=cursor.fetchall()
        ans=utilities.db_to_str(ans)
        print("conerted")
        return ans
    except Exception as e:
        print(e)
        return ''

def currentTime():
    return datetime.datetime.now()

def addUser(mac,ip,username) :
    check_DB()
    try :
        conn=utilities.connect_to_db(db_config)
        cursor=conn.cursor()
        sql="""INSERT INTO onlineUsers (mac,ip,username,last_ping) VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE last_ping = %s"""
        cursor.execute(sql,(mac,ip,username,currentTime(),currentTime()))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)

def check_DB() :
    '''try :
        conn=utilities.connect_to_db(db_config)
        cursor=conn.cursor()
        sql="""delete from onlineUsers where username='ivan' """
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print('err::::')
        print(type(e))'''

def main() :
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)
    print(f'[STARTING] Server starting')
    server.listen()
    print(f'[LISTENING] listening at {ADDR}')
    while True:
        #print('listening')
        conn,addr = server.accept()
        thread = threading.Thread(target=handleclient,args=(conn,addr))
        thread.start()

if __name__=='__main__' :
    main()
