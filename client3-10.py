import socket
from threading import Thread 

def check():
	while True:
		try:
			data = sock.recv(1024)
			msg = data.decode()
			print(msg)
		except:
			break

try:
	sock = socket.socket()
	print('Введите хост: ')
	xhost = input()
	print('Введите порт: ')
	yp = int(input())
	sock.connect((xhost, yp))
except:
	xhost = 'localhost'
	yp = 9095
	sock.connect((xhost, yp))

print("Введите пароль: ")
paswd = input()
msg = paswd
sock.send(msg.encode())

Thread(target=check).start()

while msg !="close":
	msg = input()
	if msg !='close':
		sock.send(msg.encode())


msg = 'клиент disconnected'
sock.send(msg.encode())
data = sock.recv(1024)

sock.close()