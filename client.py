import socket
import os
import time
from random import randint


class ShipWar:
	
	def __init__(self):
		self.board = []
		self.enemy_board = []
		self.Player_win = 0
		self.Enemy_win = 0
		self.debug = 0
		self.server = ('26.110.124.72',9090)
		self.server = self.get_server_info()
		self.Start_client_connection()
		pos = self.get_client_info().decode()
		ready_status = self.get_client_info().decode()

		if ready_status == 'ready':
			position_in_queue = pos

		else:
			self.disconnect()

		if position_in_queue == '1':

			try:
				width,height = self.Get_ships_and_board_info()

			except ValueError:
				self.disconnect()
			self.send_client_info([width,height])

		else:
			width,height = list(self.get_client_info())

		ships = list(self.get_client_info())
		enemy_ships = list(self.get_client_info())

		if not ships or not enemy_ships:
			self.disconnect()

		else:
			ready_status = self.get_client_info().decode()

			if ready_status == 'ready':
				self.Initializate_game_manager(width,height,ships,enemy_ships)
				self.Start_GameLoop(position_in_queue)

	def Start_GameLoop(self,pos):

		def get_answer():
			self.Print_show_boards()	
			brk = self.Search_and_get_coords()
			self.Print_show_boards()
			return brk 

		if pos == '1':
			while self.Player_win == self.Enemy_win:

				brk = get_answer()
				if brk[2] == 404:
					self.disconnect()
					break
				else:
					while True:

						if brk[2] == 1:

							if len(self.enemy_ships) == 0:
								self.send_client_info([self.Player_win,0,0,0])
								self.win(1)
								break

							self.send_client_info([self.Player_win,1,brk[0],brk[1]])
							brk = get_answer()

						if brk[2] == 2:
							self.send_client_info([self.Player_win,2,brk[0],brk[1]])
							break

				print("Ждём соперника :D")
				if self.client != 0:
					data = list(self.get_client_info())
				else:
					break

				if not data:
					self.disconnect()
					break

				if data[0] == 1:
					self.win(2)
					break
				else:
					def process_data(num,data):
						x = data[2]
						y = data[3]
						self.boardX(num,x,y)

					if data[1] == 1:

						while True:
							process_data(1,data)
							data = list(self.get_client_info())

							if data[1] == 2:
								process_data(2,data)
								break

					elif data[1] == 2:
						process_data(2,data)


		elif pos == '2':

			while self.Player_win == self.Enemy_win:
				self.Print_show_boards()
				print("Ждём соперника :D")

				if self.client != 0:
					data = list(self.get_client_info())
				else:
					break

				if not data:
					self.disconnect()
					break

				if data[0] == 1:
					self.win(2)
					break
				else:
					def process_data(num,data):
						x = data[2]
						y = data[3]
						self.boardX(num,x,y)

					if data[1] == 1:
						while True:

							process_data(1,data)
							data = list(self.get_client_info())

							if data[1] == 2:
								process_data(2,data)
								break

					elif data[1] == 2:
						process_data(2,data)

				brk = get_answer()
				if brk[2] == 404:
					self.disconnect()
					break
				else:
					while True:

						if brk[2] == 1:

							if len(self.enemy_ships) == 0:
								self.send_client_info([self.Player_win,0,0,0])
								self.win(1)
								break

							self.send_client_info([self.Player_win,1,brk[0],brk[1]])
							brk = get_answer()

						if brk[2] == 2:
							self.send_client_info([self.Player_win,2,brk[0],brk[1]])
							break

	def boardX(self,num,x,y):
		if num == 1:
			self.board[y][x] = 'X'
			self.ships.remove((x,y))

		elif num == 2:
			self.board[y][x] = '0'

	def Search_and_get_coords(self):
		while 1:
			x,y,a = self.Get_coords()
			if a == 404:
				return 0,0,404
				break
			else:
				cond = self.Check_coords(x,y)
				if cond == 1 or cond == 2:
					return x,y,cond
					break

	def Check_coords(self,x,y):

		if self.enemy_board[y][x] == '+':
			self.fake_board[y][x] = 'X'
			self.enemy_board[y][x] == 'X'
			self.enemy_ships.remove((x,y))
			print("Попадание!")
			return 1

		elif self.enemy_board[y][x] == '0':
			print("Вы уже сюда попадали!")
			return 0

		elif self.enemy_board[y][x] == 'X':
			print("Этот корабль уже повреждён!")
			return 0

		elif self.enemy_board[y][x] == ' ':
			self.fake_board[y][x] = '0'
			self.enemy_board[y][x] = '0'
			print("Мимо!")
			return 2

	def Get_coords(self):
		while 1:

			try:
				xy = list(map(int,(input('Введите X,Y |>').split())))
				if xy[0] <= len(self.board[0]) and xy[0] > 0 and xy[1] <= len(self.board) and xy[1] > 0:
					xy[0] -= 1
					xy[1] -= 1
					return xy[0],xy[1],0
				else:
					list.append()

			except TypeError:
				print("За пределы нельзя!")

			except KeyboardInterrupt:
				try:
					ans = input("Выйти?(y/n) |>")
					if ans == 'y':
						return 0,0,404
				except:
					pass

			except:
				print("Формат: Int Int")

	def Print_show_boards(self):
		os.system('cls')
		def prn():
			for a in range(len(self.board)):

				print(f' {a+1}',end="")
			print('\n')

		prn()

		k = 1
		for a in self.board:
			print(' '.join(a),end='')
			print(' ',k)
			k += 1
		prn()

		k = 1
		for a in self.fake_board:
			print(' '.join(a),end='')
			print(' ',k)
			k += 1

	def Initializate_game_manager(self,width,height,ships,enemy_ships):
		self.Create_game_board(width,height)
		self.ships,self.enemy_ships = self.Fill_game_boards(ships,enemy_ships)

	def Create_game_board(self,width,height):
		self.board = [[' ']*width for x in range(0,height)]
		self.enemy_board = [[' ']*width for x in range(0,height)]
		self.fake_board = [[' ']*width for x in range(0,height)]

	def Fill_game_boards(self,ships,enemy_ships):

		ships_construct = []
		enemy_ships_construct = []

		for a in range(0,len(ships)-1,2):
			ships_construct.append( (ships[a],ships[a+1]) )
			enemy_ships_construct.append( (enemy_ships[a],enemy_ships[a+1]) )

		for a in ships_construct:
			self.board[a[1]][a[0]] = '+'#Ship

		for a in enemy_ships_construct:
			self.enemy_board[a[1]][a[0]] = '+'

		return ships_construct,enemy_ships_construct

	def Start_client_connection(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.connect(self.server)
		print('<Connected to Server>')

	def get_client_info(self):
		return self.client.recv(1024)

	def send_client_info(self,info):

		try:
			info = info.encode()

		except:
			info = bytes(info)

		try:

			if self.client != 0:
				self.client.send(info)

			else:
				list.append()

		except ConnectionResetError:
			print('//Server stopped!//')
			self.disconnect()

		except:
			pass
	def Get_ships_and_board_info(self):
		while self.debug != 1:

			try:

				def test_value(a):
					a = int(a)
					if a <= 5:
						a = 10
					return a

				a,b = list(map(test_value,input("Введите ширину и высоту |>").split()))
				return a,b

			except ValueError:
				print("Формат!: Int Int")

			except KeyboardInterrupt:
				if self.debug == 0:
					os.system('cls')
				else:
					break

	def get_server_info(self):
		while self.debug != 1:
			try:
				info = list(map(str,input("Введите ip port |>").split()))
				a = (info[0],int(info[1]))
				return a
				break
			except:
				print("Error")
		return self.server
		
	def win(self,x):
		if x == 2:

			self.Enemy_win = 1
			print("вы проиграли!")
		else:

			self.Player_win = 1
			print("Вы выиграли!")

	def disconnect(self):
		print("//Disconnected//")
		self.client.close()
		self.client = 0
ShipWar()