import utilities
import constants
from flask import Flask,request,jsonify
import mysql.connector

DATABASE='P2P_MESSAGE_APP'
HOST='127.0.0.1'
PASSWORD='pép-server'
USER='p2p-server'
db_config={'host':HOST,
           'user':USER,
           'password':PASSWORD,
           'database':DATABASE}

def check_DB() :
    try :
        conn=connect_to_db(db_config)
        cursor=conn.cursor()
        sql="""delete from onlineUsers where (sysdate()-last_ping)>10 """
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print('err::::')
        print(type(e))

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

app=Flask(__name__)

@app.route('/')
def entry():
    html='<html> <head> <title> Hello </title> </head> <body>yo you mdf</body></html>'
    return html
@app.route('/online_users',methods=['GET'])
def onlineusers():
    check_DB()
    try :
        conn=connect_to_db(db_config)
        cursor=conn.cursor()
        print("cursor created")
        sql="""SELECT * FROM onlineUsers"""
        cursor.execute(sql)
        print("sql executed")
        ans=cursor.fetchall()
        ans=utilities.db_to_json(ans)
        print('sent user list')
        return jsonify(ans)
    except Exception as e:
        print(e)
        return ''

@app.route('/ping',methods=['POST'])
def addUser() :
    check_DB()
    try :
        conn=connect_to_db(db_config)
        cursor=conn.cursor()
        sql="""INSERT INTO onlineUsers (mac,ip,username,last_ping) VALUES (%s,%s,%s,sysdate()) ON DUPLICATE KEY UPDATE last_ping = sysdate()"""
        cursor.execute(sql,(request.json['mac'],request.json['ip'],request.json['username']))
        conn.commit()
        cursor.close()
        conn.close()
        print('added new user')
    except Exception as e:
        print(e)

#def handleclient(conn,addr):
#    connected=True
#    ip=addr[0]
#    while connected:
#        msg=utilities.recieve_msg(conn,mmac=constants.SERVER_MAC)
#        if not msg:
#            pass
#        elif msg[0]==constants.PING_MSG:
#            addUser(mac=msg[2],username=msg[1],ip=ip)
#        elif msg[0]==constants.GET_USER_LIST:
#            utilities.sendmsg(onlineusers(),conn,'MAIN_SERVER',constants.SERVER_MAC,msg[2])
#            print(f'sent to {msg[2]},{ip}')
#        else :
#            print(msg)
#    conn.close()

def main() :
    check_DB()
#    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#    server.bind(ADDR)
#    print(f'[STARTING] Server starting')
#    server.listen()
#    print(f'[LISTENING] listening at {ADDR}')
#    while True:
        #print('listening')
#        conn,addr = server.accept()
#        thread = threading.Thread(target=handleclient,args=(conn,addr))
#        thread.start()
    app.run(debug=True)
if __name__=='__main__' :
    main()
