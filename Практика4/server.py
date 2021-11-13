import threading
from contextlib import closing
from os import remove
import socket
from bcrypt import checkpw, hashpw, gensalt

class ConnThread(threading.Thread):
    def __init__(self, con, adr):
        super().__init__(daemon=True)
        self.con = con
        self.adr = adr
        self.connected = False
        self.whos = ''
    def login(self):
        try:
            start('user '+self.adr[0]+' connect') 
            for i in spic:
                if str(self.adr) == str(i):
                    while True:
                        name = spic[i]
                        sender(self.con, 'Здравствуйте, '+name+'. Введите ваш пароль')
                        msg = addressee(self.con)
                        file = open('pas'+name+'.bin', "rb")
                        key = file.read()
                        file.close()
                        if checkpw(bytes(msg, encoding='utf-8'), key):
                            key=''
                            msg=''
                            sender(self.con, 'Пароль принят')
                            start('user '+name+' enter the conf')
                            break
                        else:
                            key=''
                            sender(self.con, 'Неверный пароль')
                    break
            else:  
                sender(self.con, 'Здравствуйте, новый пользователь. Представьтесь, пожалуйста')
                name = addressee(self.con)
                sender(self.con, "Введите ваш пароль")
                key = addressee(self.con)
                key = hashpw(bytes(key, encoding='utf-8'), gensalt())
                with open("pas"+str(name)+".bin", "wb") as file:
                    file.write(key)
                key=''
                with open("users_2.txt", "a") as file:
                    file.write(str(self.adr)+' NaMe '+str(name)+'\n')
                spic.update({self.con: name}) 
            self.connected = True
            sender(self.con, 'Спасибо')
            connect.append(self.con)
            
            self.whos = name
        except ConnectionResetError:
            pass
    def run(self):
        while True:
            if work and self.connected == False and self.whos != False:
                self.whos = False
                try:
                    loggg = threading.Thread(target=self.login)
                    loggg.start()
                except ConnectionResetError:
                    continue
            while self.connected and work:
                try:
                    msg = addressee(self.con)
                    
                    if msg == 'exit':
                        self.connected = False
                        connect.remove(self.con)
                        start('user '+self.whos+' exit')
                    elif work:
                        start('received message from '+self.whos)
                        msg = '{'+self.whos+'}: '+msg
                        for i in connect:
                            if i != self.con:
                                try:
                                    sender(i, msg)
                                except ConnectionResetError:
                                    del(connect[connect.index(i)])
                        with open(st_file, 'a') as f:
                            f.write(msg+'\n')
                except ConnectionResetError:
                    del(connect[connect.index(i)])
                    break
                
def start (sb):#, nom
    f = open(nameOfLog, 'a')
    f.write(sb+'\n')
    f.close()
def vvod (maxx, value, stand):
        while True:
                chis = input("Введите " +value+ " или stand для значения по умолчанию = "+str(stand)+ ": ")
                if chis.isdigit(): #0-65535
                        chis = int(chis)
                        if chis > -1 and chis < maxx+1:
                                return (chis)
                        else:
                                print("Введите чисто от 0 до " + str(maxx))
                elif chis == "stand":
                        return(stand)
                else:
                        print("Введите целове число")
def free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
def addressee(who):
    '''while work==False:
        continue#'''
    msg = who.recv(1024).decode()
    return msg
def sender(andere, msg):
    #if work:
    andere.send(msg.encode('utf-8'))





connect=[]
spic={}
with open('users_2.txt', 'r') as file:
    for line in file:#file.write(str(addr)+' NAME '+str(name)+'\n')
        nom = line.split(' NAME ')
        spic.update({nom[0]: nom[1][:-1]}) 
        
#file.close()
sock = socket.socket()
nom = vvod(65535, "ваш порт", 53480)
try:
        sock.bind(('', nom))
except OSError:
        nom = free_port()
        print('Выбранный вами код сервера уже занят, код сервера будет изменён автоматически. Новый код: ', nom)
        sock.bind(('', nom))

nameOfLog = 'log_server'+str(nom)+'.txt'
with open(nameOfLog, 'w') as f:
    f.write('Server activate\nvash port servera - '+str(nom)+ '\n')
st_file='story_let'+str(nom)+'.txt'
with open(st_file, 'w') as f:
    f.write('')
#f.close()

sock.listen(4)
work=True
def sozd_thr(sock):
    while work:
        try:
            potok = ConnThread(*sock.accept())
            potok.start()
        except OSError:
            break

gen_th = threading.Thread(target=sozd_thr, args=[sock])
gen_th.start()

#sozd_thr(sock)

while True:
    comm = input('exit - Отключение сервера, showstor - история сообщений, pause - остановка прослушивание порта, showlog - Показ логов, clearlog - Очистка логов, killusers - Очистка файла идентификации: ')
    if 'showlog' == comm:
        with open(nameOfLog, 'r') as f:#st_file
            for i in f:
                print(i, end='')
    elif 'showstor' == comm:
        with open(st_file, 'r') as f:#st_file
            for i in f:
                print(i, end='')
    elif 'clearlog' == comm:
         with open(nameOfLog, 'w') as f:
             f.write('logs clear\n')
    elif 'killusers' == comm:
        work = False
        start('Users deleted')
        for line in spic:
            remove("pas"+spic[line]+".bin")
        with open('users_2.txt', 'w') as file:
            file.write('')
        work = True
    elif 'exit' == comm:
        #nstopot=False
        work = False
        start('end of work')
        sock.close()
        break
    elif 'pause' == comm:
        if work:
            work = False
            print('Сервер поставлен на паузу. Для продолжения работы введите pause повторно')
            start('server on pause')
        else:
            work = True
            print('Сервер снят с паузы.')
            start('end of pause')
    else:
        print('Команда не распознана.')