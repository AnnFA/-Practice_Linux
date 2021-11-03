import socket
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

from contextlib import closing
def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
def otprav(file, sock, msg):
        #msg = input()
        dlin = len(msg)
        sock.send((str(dlin)+' '*(6-len(str(dlin)))+msg).encode())
        try:
                sock.recv(1024)
        except ConnectionAbortedError:
                file.write('Ошибка. Подключение разорвано')
                return(False)
        else:
                #msg = data.decode() #sock.send(data) #return(msg)
                return(True)

file = open('log_client.txt', 'w')
#file.write('')
sock = socket.socket()
nport = vvod(65535, "vash port", 52865)#62670
file.write('vash port - '+str(nport)+'\n')
try:
        sock.bind(('', nport))
except OSError:
        nom = find_free_port()
        print('Ошибка. Выбранный код занят, код сервера будет изменён. Новый код: ', nport)
        sock.bind(('', nport))
    
sock.setblocking(1)
nom_pod = vvod(65535, "port podkluchenia", 53480)
file.write('port podkluchenia - '+str(nom_pod)+'\n')
ipe =''
ipeym = [127, 0, 0, 1]
for i in range (4):
        ipe += str(vvod(255, str(i+1)+" element ip", ipeym[i]))+'.'
ipe = ipe[:-1]
file.write('ip podkluchenia - '+str(ipe)+'\n')
sock.connect((ipe, nom_pod))

def  poluch(sock):
        data = sock.recv(1024)
        msg = data.decode()
        sock.send(data)
        return(msg)
msg = poluch(sock)
print(msg)
if msg == 'Здравствуйте, новый клиент. Представьтесь, пожалуйста ':
        otprav(file, sock, input())
        print(poluch(sock))
        otprav(file, sock, input())
        print(poluch(sock))
else:
        msg = 'Неверный пароль'
        while msg == 'Неверный пароль':
                print(poluch(sock))
                otprav(file, sock, input())
                msg = poluch(sock)
                print(msg)
while True:
        msg = input('Msg: ')
        if otprav(file, sock, msg)==False or msg == "exit":
                break
sock.close()
file.write("exit")
file.close()