import socket

class Connessione():
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = "192.168.1.2"
		self.port = 5555
		self.addr = (self.server, self.port)
		self.pos = self.connect()

	def connect(self):
		try:
			self.client.connect(self.addr)
			return self.client.recv(2048).decode()
		except:
			pass

	def send(self, data):
		try:
			self.client.send(str.encode(data))
			return self.client.recv(2048).decode()
		except socket.error as e:
			return None