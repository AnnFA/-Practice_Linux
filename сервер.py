import socket
import bcrypt

def vvod (maks, vv, stand):
        while True:
                chis = "stand"
                #chis = input("введите" +vv+ " или stand для получения значения по умолчанию "+str(stand)+ ": ")
                if chis.isdigit(): #0 - 65535
                        chis = int(chis)
                        if chis > -1 and chis < maks+1:
                                return (chis)
                        else:
                                print("введите число от 0 до " + str(maks))
                elif chis == "stand":
                        return(stand)
                else:
                        print("введите целое число")
#'''
from contextlib import closing
def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
#'''
#file = open('users.txt', 'a')

f = open('log_server.txt', 'w') 
sock = socket.socket()
nport = vvod(65535, "vash port", 53480)
f.write('vash port - '+str(nport)+'\n')

try:
        sock.bind(('', nport))
except OSError:
        nom = find_free_port()
        print('Ошибка. Выбранный код сервера уже занят, код будет изменён. Новый код: ', nport)
        sock.bind(('', nport))

sock.listen(0)
#conn, addr = sock.accept()
#print('Соединено: '+str(addr))
#file.write(str(addr)+'\n')
#msg = ''
#addr2 = str(addr)
spic=[]
file = open('users_2.txt', 'r')
for line in file:
        spic.append(line.split(' NaMe '))
        
file.close()

def otpravlenie(file, sock, msg):
        sock.send(msg.encode())
        try:
                sock.recv(1024)    
        except ConnectionAbortedError:
                file.write('Ошибка. Подключение разорвано')
                return(False)
        else:
                #msg = data.decode()  #sock.send(data) #return(msg)
                return(True)
def  poluchenie(sock, file):
        data = sock.recv(1024)
        msg = data.decode()
        sock.send(data)
        return(msg[6:])
def prov(f, conn, name, addr):        #name = line[1]
    file = open("pas"+name+".bin", "rb")
    key = file.read()
    file.close()
    if otpravlenie(f, conn, 'Приветствую, '+name):
        while True:
            otpravlenie(f, conn, 'Введите ваш пароль')
            msg = poluchenie(conn, f)
            if bcrypt.checkpw(bytes(msg, encoding='utf-8'), key):
                if otpravlenie(f, conn, 'Пароль принят'):
                    msg=pepepic (conn, addr, f, name)
                    return(msg)
                else:
                    break
                                            
            elif otpravlenie(f, conn, 'Неверный пароль')==False:
                break
    return('dis')
def pepepic (conn, addr, file, name):
        addr2 = str(addr)
        while True:
                try:
                        data = conn.recv(1024)
                except (ConnectionResetError, OSError):
                        conn, addr = sock.accept()
                        if str(addr) != addr2:
                                conn.close()
                        else:
                            return(prov(file, conn, name, addr))
                else:
                        msg = data.decode()
                        conn.send(data)
                        dlin = msg[:6]
                        print('Получено сообщение длиной '+dlin+' символов: ')
                        file.write('Получено сообщение длиной '+dlin+' символов: ')
                        msg = msg[6:]
                        if data:
                                if msg == "dis" or msg == "exit":
                                        return(msg)
                                print(msg)
while True:
        conn, addr = sock.accept()
        print('Соединено: '+str(addr))
        f.write(str(addr)+'\n')
    
        for line in spic:
                if line[0] == str(addr):
                        name=line[1][:-1]
                        msg=prov(f, conn, name, addr)
                        break
        else:
                if otpravlenie(f, conn, 'Здравствуйте, новый клиент. Представьтесь, пожалуйста'):
                        name = poluchenie(conn, f)
                        if otpravlenie(f, conn, 'Введите ваш пароль'):
                                key = poluchenie(conn, f)
                                key = bcrypt.hashpw(bytes(key, encoding='utf-8'), bcrypt.gensalt())#'''
                                file = open("users_2.txt", "a")
                                file.write(str(addr)+' NaMe '+str(name)+'\n')
                                file.close()
                                file = open("pas"+str(name)+".bin", "wb")
                                file.write(key)
                                file.close()
                                f.write('User '+str(name)+' add''+\n')
                                spic.append([str(addr), msg])
                                otpravlenie(f, conn, 'Спасибо')
                                print('Имя и пароль сохранены')
                                msg = pepepic (conn, addr, f, name)
        conn.close()
        if msg == "exit":
            break
f.write('exit')
file.close()