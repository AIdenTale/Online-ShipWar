from random import randint
import socket
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
while 1:
	try:
		info = list(map(str,input("Введите ip port |>").split()))
		a = (info[0],int(info[1]))
			break
		except:
			print("Error")
server_socket.bind(a)
server_socket.listen(2)
print("Server started!")

def WaitForConnect(server_socket):

	clients = {}

	for a in range(2):
		client_socket,addr = server_socket.accept()
		clients[addr] = client_socket
		clients[addr].send(str(a+1).encode())
		print(addr,"<Connected to server_socket>")

	return clients,addr

def Start_server(server_socket):

	print("Waiting for connecting 2 clients...")
	clients,last_client = WaitForConnect(server_socket)

	for a in clients:
		clients[a].send('ready'.encode())

	a = 0
	for client in clients:

		if a == 0:
			width,height = list(clients[client].recv(1024))
			first = client
			print("Width:",width,"height:",height)
			clients[last_client].send(bytes([width,height]))
			break
		a += 1

	ships_to_send = create_coords(width,height)

	for client in clients:

		for a in range(2):
			clients[client].send(bytes(ships_to_send[a]))

		ships_to_send.reverse()
		clients[client].send('ready'.encode())
	err = 0
	while err == 0:

		win = 0
		while err == 0:

			try:
				data = list(clients[first].recv(1024))
				win = 1
				print('To',last_client,'>',data)
				clients[last_client].send(bytes(data))
				print(data)
				if data[1] == 1:
					pass
				else:
					break

			except:
				print('Cliend droped')
				clients[first].close()
				err = 1
				break

		while err == 0:

			try:
				data = list(clients[last_client].recv(1024))
				win = 2
				print('To',first,'>','\n',data)
				clients[first].send(bytes(data))
				print(data)

				if data[1] == 1:
					pass

				else:
					break

			except:
				print('Cliend droped')
				clients[first].close()
				err = 1
				break
		if err == 0 and data[0] == 1:

			if win == 1:
				print('Win first')
				
			else:
				print('Win second')

def create_coords(width,height):
	ships = []
	send = []
	def get_coords():
		send = []
		for a in range( round( (width+height)/2-2 )):
			while 1:
				x = randint(0,width-1)
				y = randint(0,height-1)
				if (x,y) not in ships:
					send.append(x)
					send.append(y)
					ships.append((x,y))
					break
		return send
	send.append(get_coords())
	send.append(get_coords())
	print(send)
	print("Ships 1 client:\n",send[0],"\nShips 2 client:\n",send[1])
	return send

Start_server(server_socket)
