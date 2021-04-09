import socket

class Connessione():
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = "87.250.73.23"
		self.port = 8100
		self.addr = (self.server, self.port)
		self.pos = self.connect()

	def connect(self):
		try:
			self.client.connect(self.addr)
			return self.client.recv(2048).decode()
		except Exception as e:
			print("Impossibile connettersi al server")
			print(str(e))

	def send(self, data):
		try:
			self.client.send(str.encode(data))
			return self.client.recv(2048).decode()
		except socket.error as e:
			str(e)
			return None